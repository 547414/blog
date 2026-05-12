from html import escape
from html.parser import HTMLParser
from typing import List, Optional, Tuple
from urllib.parse import unquote, urlsplit

from basic.minio_client.minio_client import MinioClient


class RichTextImageUrlParser(HTMLParser):
    def __init__(self, minio_client: MinioClient):
        super().__init__(convert_charrefs=False)
        self.__minio_client = minio_client
        self.__html_part_list: List[str] = []

    def handle_starttag(self, tag: str, attrs):
        self.__html_part_list.append(
            f"<{tag}{self.__format_attr_list(tag=tag, attrs=attrs)}>"
        )

    def handle_startendtag(self, tag: str, attrs):
        self.__html_part_list.append(
            f"<{tag}{self.__format_attr_list(tag=tag, attrs=attrs)} />"
        )

    def handle_endtag(self, tag: str):
        self.__html_part_list.append(f"</{tag}>")

    def handle_data(self, data: str):
        self.__html_part_list.append(data)

    def handle_entityref(self, name: str):
        self.__html_part_list.append(f"&{name};")

    def handle_charref(self, name: str):
        self.__html_part_list.append(f"&#{name};")

    def handle_comment(self, data: str):
        self.__html_part_list.append(f"<!--{data}-->")

    def handle_decl(self, decl: str):
        self.__html_part_list.append(f"<!{decl}>")

    def handle_pi(self, data: str):
        self.__html_part_list.append(f"<?{data}>")

    def get_html(self) -> str:
        return "".join(self.__html_part_list)

    def __format_attr_list(self, tag: str, attrs) -> str:
        attr_part_list = []
        for attr_name, attr_value in attrs:
            if tag.lower() == "img" and attr_name.lower() == "src" and attr_value:
                attr_value = self.__refresh_image_url(src=attr_value)
            if attr_value is None:
                attr_part_list.append(attr_name)
            else:
                attr_part_list.append(f'{attr_name}="{escape(attr_value, quote=True)}"')
        if not attr_part_list:
            return ""
        return " " + " ".join(attr_part_list)

    def __refresh_image_url(self, src: str) -> str:
        object_info = self.__get_object_info(src=src)
        if not object_info:
            return src
        bucket_name, object_name = object_info
        try:
            return self.__minio_client.get_file_url(
                bucket_name=bucket_name,
                object_name=object_name,
            )
        except Exception:
            return src

    def __get_object_info(self, src: str) -> Optional[Tuple[str, str]]:
        source = src.strip()
        if not source:
            return None
        source_lower = source.lower()
        if source_lower.startswith(("data:", "blob:", "javascript:", "mailto:")):
            return None

        parsed_url = urlsplit(source)
        if parsed_url.netloc and not self.__is_minio_url(netloc=parsed_url.netloc):
            return None

        object_path = unquote(parsed_url.path).lstrip("/")
        if not object_path:
            return None

        if parsed_url.netloc:
            path_part_list = object_path.split("/", 1)
            if len(path_part_list) != 2:
                return None
            return path_part_list[0], path_part_list[1]

        default_bucket_name = self.__minio_client.default_bucket_name
        if not default_bucket_name:
            return None
        return default_bucket_name, object_path

    def __is_minio_url(self, netloc: str) -> bool:
        minio_endpoint = self.__minio_client.endpoint
        parsed_endpoint = urlsplit(
            minio_endpoint if "://" in minio_endpoint else f"//{minio_endpoint}"
        )
        return netloc == (parsed_endpoint.netloc or parsed_endpoint.path)


def refresh_rich_text_image_url(content: Optional[str], minio_client: MinioClient) -> Optional[str]:
    if not content:
        return content
    parser = RichTextImageUrlParser(
        minio_client=minio_client,
    )
    try:
        parser.feed(content)
        parser.close()
        return parser.get_html()
    except Exception:
        return content

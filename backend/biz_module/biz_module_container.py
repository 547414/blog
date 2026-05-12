from dependency_injector import containers, providers

from basic_module.basic_module_container import BasicModuleContainer
from biz_module.repository.wiki_page_file_repository import WikiPageFileRepository
from biz_module.repository.wiki_page_repository import WikiPageRepository
from biz_module.repository.wiki_project_repository import WikiProjectRepository
from biz_module.service.wiki_page_file_service import WikiPageFileService
from biz_module.service.wiki_page_service import WikiPageService
from biz_module.service.wiki_project_service import WikiProjectService


class BizModuleContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    basic_module_container = providers.Container(BasicModuleContainer)
    # 引用 BasicModuleContainer 中的单例
    session = basic_module_container.session
    minio_client = basic_module_container.minio_client
    unit_of_work = basic_module_container.unit_of_work

    wiki_page_repository = providers.Factory(
        WikiPageRepository,
        session=session,
    )

    wiki_page_file_repository = providers.Factory(
        WikiPageFileRepository,
        session=session,
    )

    wiki_project_repository = providers.Factory(
        WikiProjectRepository,
        session=session,
    )

    wiki_page_service = providers.Factory(
        WikiPageService,
        wiki_page_repository=wiki_page_repository,
        wiki_project_repository=wiki_project_repository,
        minio_client=minio_client,
    )

    wiki_page_file_service = providers.Factory(
        WikiPageFileService,
        wiki_page_file_repository=wiki_page_file_repository,
    )

    wiki_project_service = providers.Factory(
        WikiProjectService,
        wiki_project_repository=wiki_project_repository,
    )

import {AxiosResponse} from "axios";

export const getFileNameFromHeaders = (headers: any) => {
    const contentDisposition = headers['content-disposition'];
    let fileName = null;

    if (contentDisposition) {
        // 支持 filename* 和 filename 的格式
        const filenameRegex = /filename\*=(?:UTF-8'')?([^;]+)|filename="?([^"]+)"?/i;
        const matches = contentDisposition.match(filenameRegex);

        if (matches) {
            // 优先使用 filename* 的值
            fileName = matches[1] ? decodeURIComponent(matches[1]) : matches[2];
        }
    }

    return fileName;
};

export const downloadFileByA = (res: AxiosResponse<Blob>) => {
    const url = window.URL.createObjectURL(res.data); // 创建 Blob URL
    const link = document.createElement('a'); // 创建 <a> 标签
    link.href = url;
    link.download = getFileNameFromHeaders(res.headers); // 设置文件名
    document.body.appendChild(link); // 添加到 DOM
    link.click(); // 触发点击事件下载文件
    link.remove(); // 下载完成后移除链接
    window.URL.revokeObjectURL(url); // 释放 Blob URL
}

/**
 * 直接下载远程 URL 的文件，处理跨域情况
 */
export const downloadFromUrl = async (url: string | null | undefined, fileName?: string | null) => {
    if (!url) return
    const safeName = fileName || (() => {
        try { return decodeURIComponent(new URL(url).pathname.split('/').pop() || 'download') }
        catch { return 'download' }
    })()
    try {
        const response = await fetch(url)
        if (!response.ok) throw new Error('fetch failed')
        const blob = await response.blob()
        const blobUrl = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = blobUrl
        link.download = safeName
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(blobUrl)
    } catch {
        // 降级：直接新窗口打开
        window.open(url, '_blank')
    }
}
import logging
import traceback

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from basic.api_response.api_response import ApiResponse
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.repository.unit_of_work import UnitOfWork
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.utils.union_user_auth_util import validate_token
from biz_module.model.wiki_page_model import (
    EditWikiPageParamsModel,
    DeleteWikiPageParamsModel,
    SetWikiPageVisibilityParamsModel,
    SaveWikiPageTreeParamsModel,
)
from biz_module.model.wiki_page_file_model import (
    SaveWikiPageFileParamsModel,
    DeleteWikiPageFileParamsModel,
    GetWikiPageFileListParamsModel,
)
from biz_module.service.wiki_page_file_service import WikiPageFileService
from biz_module.service.wiki_page_service import WikiPageService
from biz_module.service.wiki_project_service import WikiProjectService

router = APIRouter()
logger = logging.getLogger('wiki_page')


@router.get('/public/tree')
@inject
def route_wiki_page_public_tree(
        request: Request,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        ),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            project = wiki_project_service.ensure_home_project()
            tree = wiki_page_service.get_public_tree(project_id=project.id)
            result.data = [item.model_dump() for item in tree]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/public/tree/{project_id}')
@inject
def route_wiki_page_public_project_tree(
        request: Request,
        project_id: str,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            tree = wiki_page_service.get_public_tree(project_id=project_id)
            result.data = [item.model_dump() for item in tree]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/public/search')
@inject
def route_wiki_page_public_search(
        request: Request,
        search: str = Query(''),
        page: int = Query(1),
        page_size: int = Query(20, alias='pageSize'),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        ),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            wiki_project_service.ensure_home_project()
            data_list = wiki_page_service.search_public_list(
                search=search,
                page=page,
                page_size=page_size,
            )
            result.data = data_list.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/public/detail/{page_id}')
@inject
def route_wiki_page_public_detail(
        request: Request,
        page_id: str,
        auth_code: str = Query(None, alias='authCode'),
        project_id: str = Query(None, alias='projectId'),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            page = wiki_page_service.get_public_detail(
                page_id=page_id,
                auth_code=auth_code,
                project_id=project_id,
            )
            result.data = page.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/public/file/list/{page_id}')
@inject
def route_wiki_page_public_file_list(
        request: Request,
        page_id: str,
        auth_code: str = Query(None, alias='authCode'),
        project_id: str = Query(None, alias='projectId'),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        ),
        wiki_page_file_service: WikiPageFileService = Depends(
            Provide[Container.biz_module_container.wiki_page_file_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            wiki_page_service.get_public_detail(
                page_id=page_id,
                auth_code=auth_code,
                project_id=project_id,
            )
            file_list = wiki_page_file_service.get_list(
                params=GetWikiPageFileListParamsModel(page_id=page_id)
            )
            result.data = [f.model_dump() for f in file_list]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/tree')
@inject
def route_wiki_page_tree(
        request: Request,
        project_id: str = Query(None, alias='projectId'),
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        ),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={'project_id': project_id},
        )
        with uow:
            if not project_id:
                project_id = wiki_project_service.ensure_home_project().id
            tree = wiki_page_service.get_tree(project_id=project_id)
            result.data = [item.model_dump() for item in tree]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/detail/{page_id}')
@inject
def route_wiki_page_detail(
        request: Request,
        page_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={'page_id': page_id},
        )
        with uow:
            page = wiki_page_service.get_detail(page_id=page_id)
            result.data = page.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/edit')
@inject
def route_wiki_page_edit(
        request: Request,
        params: EditWikiPageParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        ),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            if not params.project_id:
                params.project_id = wiki_project_service.ensure_home_project().id
            page_id = wiki_page_service.edit(
                params=params,
                current_user_info=current_user_info,
            )
            result.data = page_id
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/delete')
@inject
def route_wiki_page_delete(
        request: Request,
        params: DeleteWikiPageParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            wiki_page_service.delete(params=params)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/file/save')
@inject
def route_wiki_page_file_save(
        request: Request,
        params: SaveWikiPageFileParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_file_service: WikiPageFileService = Depends(
            Provide[Container.biz_module_container.wiki_page_file_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            file_id = wiki_page_file_service.save(
                params=params,
                current_user_info=current_user_info,
            )
            result.data = file_id
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/file/list')
@inject
def route_wiki_page_file_list(
        request: Request,
        params: GetWikiPageFileListParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_file_service: WikiPageFileService = Depends(
            Provide[Container.biz_module_container.wiki_page_file_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            file_list = wiki_page_file_service.get_list(params=params)
            result.data = [f.model_dump() for f in file_list]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/file/delete')
@inject
def route_wiki_page_file_delete(
        request: Request,
        params: DeleteWikiPageFileParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_file_service: WikiPageFileService = Depends(
            Provide[Container.biz_module_container.wiki_page_file_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            wiki_page_file_service.delete(params=params)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/visibility/set')
@inject
def route_wiki_page_visibility_set(
        request: Request,
        params: SetWikiPageVisibilityParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            wiki_page_service.set_visibility(params=params)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/history/list/{page_id}')
@inject
def route_wiki_page_history_list(
        request: Request,
        page_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={'page_id': page_id},
        )
        with uow:
            result.data = []
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/tree/save')
@inject
def route_wiki_page_tree_save(
        request: Request,
        params: SaveWikiPageTreeParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_page_service: WikiPageService = Depends(
            Provide[Container.biz_module_container.wiki_page_service]
        ),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params=params.model_dump(),
        )
        with uow:
            if not params.project_id:
                params.project_id = wiki_project_service.ensure_home_project().id
            wiki_page_service.save_tree(params=params)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())

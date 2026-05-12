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
from biz_module.model.wiki_project_model import (
    EditWikiProjectParamsModel,
    DeleteWikiProjectParamsModel,
    WikiProjectPageParamsModel,
)
from biz_module.service.wiki_project_service import WikiProjectService

router = APIRouter()
logger = logging.getLogger('wiki_project')


@router.get('/public/page')
@inject
def route_wiki_project_public_page(
        request: Request,
        page_index: int = Query(1, alias='pageIndex'),
        page_size: int = Query(12, alias='pageSize'),
        search: str = Query(None),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            project_page = wiki_project_service.get_public_page(
                params=WikiProjectPageParamsModel(
                    page_index=page_index,
                    page_size=page_size,
                    search=search,
                )
            )
            result.data = project_page.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/public/detail/{project_id}')
@inject
def route_wiki_project_public_detail(
        request: Request,
        project_id: str,
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            project = wiki_project_service.get_by_id(project_id=project_id)
            result.data = project.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/home')
@inject
def route_wiki_project_home(
        request: Request,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        with uow:
            project = wiki_project_service.ensure_home_project()
            result.data = project.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/list')
@inject
def route_wiki_project_list(
        request: Request,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
        wiki_project_service: WikiProjectService = Depends(
            Provide[Container.biz_module_container.wiki_project_service]
        )
):
    result = ApiResponse()
    try:
        uow.init_log_data(
            current_user_info=current_user_info.model_dump(),
            request_info=FastApiRequestForLogModel.init(request=request),
            request_params={},
        )
        with uow:
            project_list = wiki_project_service.get_list()
            result.data = [project.model_dump() for project in project_list]
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.get('/detail/{project_id}')
@inject
def route_wiki_project_detail(
        request: Request,
        project_id: str,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
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
            project = wiki_project_service.get_by_id(project_id=project_id)
            result.data = project.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/page')
@inject
def route_wiki_project_page(
        request: Request,
        params: WikiProjectPageParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
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
            project_page = wiki_project_service.get_page(params=params)
            result.data = project_page.model_dump()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/edit')
@inject
def route_wiki_project_edit(
        request: Request,
        params: EditWikiProjectParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
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
            project_id = wiki_project_service.edit(
                params=params,
                current_user_info=current_user_info,
            )
            result.data = project_id
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())


@router.post('/delete')
@inject
def route_wiki_project_delete(
        request: Request,
        params: DeleteWikiProjectParamsModel,
        current_user_info: ValidateTokenResModel = Depends(validate_token),
        uow: UnitOfWork = Depends(Provide[Container.basic_module_container.unit_of_work]),
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
            wiki_project_service.delete(params=params)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        result = ApiResponse(code=500, message=str(e))
    return JSONResponse(content=result.to_json())

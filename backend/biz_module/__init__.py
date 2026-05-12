from biz_module.biz_module_container import BizModuleContainer
from config.config import Config

biz_module_container = BizModuleContainer()
biz_module_container.config.from_dict(Config().model_dump())

biz_module_container.wire(packages=[__name__])

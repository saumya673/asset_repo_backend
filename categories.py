from enum import StrEnum


class Service(StrEnum):
    OPS = "Ops"
    AD = "AD"
    QE = "QE"
    SD = "SD"
    EUC = "EUC"


class Domain(StrEnum):
    ECOMMERCE_ONLINE = "Ecommerce/online"
    MERCHANDISING = "Merchandising"
    SUPPLY_CHAIN = "Supply Chain"
    STORES = "Stores"
    FINANCE = "Finance"
    HR = "HR"
    MARKETING_CUSTOMER = "Marketing/Customer"
    DATA = "Data"
    INTEGRATION = "Integration"
    CYBER_SECURITY = "Cyber Security"
    TECHNOLOGY_PLATFORM = "Technology Platform (IDP, CICD, K8s, Observability)"
    CLOUD = "Cloud"
    INFRA = "Infra"
    ENTERPRISE = "Enterprise"


class Scope(StrEnum):
    OPERATING_MODEL_TRANSFORMATION = "Operating model transformation"
    TECH_MODERNIZATION = "Tech Modernization"
    MIGRATION = "Migration"
    OPS_TRANSFORMATION = "Ops transformation"
    AI_INFUSION = "AI infusion"


class ProjectType(StrEnum):
    SUCCESS_STORY = "Success story"
    CASE_STUDY = "case study"
    AI_AGENT = "ai agent"
    TOOL_UTILITY = "tool/utility"
    BOT = "Bot"
    FRAMEWORK = "framework"
    WHITEPAPER = "whitepaper"


SERVICE_VALUES = [item.value for item in Service]
DOMAIN_VALUES = [item.value for item in Domain]
SCOPE_VALUES = [item.value for item in Scope]
TYPE_VALUES = [item.value for item in ProjectType]
TAG_VALUES = SERVICE_VALUES + DOMAIN_VALUES + SCOPE_VALUES + TYPE_VALUES

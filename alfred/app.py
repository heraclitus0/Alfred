from __future__ import annotations
from dotenv import load_dotenv
from alfred.core.runtime import AlfredRuntime
from alfred.storage.db import Database
from alfred.memory.base import MemoryFacade
from alfred.consultation.manager import ConsultationManager
from alfred.research_threads.manager import ResearchThreadManager
from alfred.prompts.prompt_engineer import PromptEngineer
from alfred.llm.openai_client import OpenAIConsultClient
from alfred.actions.browser.operator import BrowserOperator
from alfred.actions.projects.sandbox_manager import SandboxManager
from alfred.self_improvement.diagnostics import DiagnosticsEngine
from alfred.self_improvement.weakness_detector import WeaknessDetector
from alfred.self_improvement.proposal_builder import ProposalBuilder
from alfred.self_improvement.sandbox_runner import SelfRewriteSandbox
from alfred.self_improvement.promoter import PromotionManager
from alfred.autonomy.approval_engine import ApprovalEngine
from alfred.safety.audit import AuditLogger
from alfred.safety.kill_switch import KillSwitch
from alfred.missions.manager import MissionManager
from alfred.notifications.manager import NotificationManager
from alfred.watchers.manager import WatcherManager
from alfred.user_model.primary_core import PrimaryCore


def build_runtime() -> AlfredRuntime:
    load_dotenv()
    db = Database()
    db.init()
    memory = MemoryFacade(db)
    thread_manager = ResearchThreadManager(memory)
    prompt_engineer = PromptEngineer()
    llm_client = OpenAIConsultClient()
    browser = BrowserOperator()
    sandbox = SandboxManager()
    diagnostics = DiagnosticsEngine(memory)
    weakness = WeaknessDetector(diagnostics)
    proposal_builder = ProposalBuilder(prompt_engineer, llm_client)
    rewrite_sandbox = SelfRewriteSandbox(sandbox)
    promoter = PromotionManager(memory)
    approvals = ApprovalEngine()
    audit = AuditLogger(memory)
    kill_switch = KillSwitch(memory)
    missions = MissionManager(memory)
    notifications = NotificationManager(memory)
    watchers = WatcherManager(memory, notifications)
    primary = PrimaryCore(memory)
    consultation = ConsultationManager(
        memory=memory,
        thread_manager=thread_manager,
        prompt_engineer=prompt_engineer,
        llm_client=llm_client,
        browser=browser,
        notifications=notifications,
        audit=audit,
    )
    runtime = AlfredRuntime(
        memory=memory,
        consultation=consultation,
        thread_manager=thread_manager,
        browser=browser,
        mission_manager=missions,
        notification_manager=notifications,
        watcher_manager=watchers,
        approval_engine=approvals,
        diagnostics=diagnostics,
        weakness_detector=weakness,
        proposal_builder=proposal_builder,
        rewrite_sandbox=rewrite_sandbox,
        promoter=promoter,
        audit=audit,
        kill_switch=kill_switch,
        primary_core=primary,
    )
    return runtime

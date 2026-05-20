import unittest

from app.agents.reasoning_engine import ReasoningEngine


class TestAgentReasoning(unittest.IsolatedAsyncioTestCase):
    async def test_legal_email_triggers_legal_escalation(self):
        classification = {
            "category": "Legal",
            "sentiment": "Negative",
            "confidence": 0.97,
            "urgency": "Critical",
            "requires_human": True,
            "escalation_reason": "Contains lawsuit threat and legal review request.",
        }

        state = await ReasoningEngine.reason(
            email_id="550e8400-e29b-41d4-a716-446655440000",
            thread_id="660e8400-e29b-41d4-a716-446655440001",
            classification=classification,
            sender_email="bob.jones@enterprise.net",
            email_subject="Notice of Legal Action",
            email_body="This is a legal notice. We require a formal response before the end of the day.",
        )

        self.assertTrue(state.should_escalate)
        self.assertEqual(state.final_decision, "escalate_to_human")
        self.assertEqual(len(state.reasoning_trace), 1)
        self.assertEqual(state.reasoning_trace[0].tool_call.tool_name, "flag_for_legal")

    async def test_billing_email_includes_account_check_and_knowledge_search(self):
        classification = {
            "category": "Billing",
            "sentiment": "Neutral",
            "confidence": 0.88,
            "urgency": "Medium",
            "requires_human": False,
        }

        state = await ReasoningEngine.reason(
            email_id="550e8400-e29b-41d4-a716-446655440002",
            thread_id="660e8400-e29b-41d4-a716-446655440003",
            classification=classification,
            sender_email="customer@example.com",
            email_subject="Invoice inquiry",
            email_body="Please clarify why my latest invoice is higher than expected.",
        )

        self.assertFalse(state.should_escalate)
        self.assertEqual(state.final_decision, "send_auto_reply")
        self.assertTrue(any(step.tool_call and step.tool_call.tool_name == "check_account_status" for step in state.reasoning_trace))
        self.assertTrue(any(step.tool_call and step.tool_call.tool_name == "search_knowledge_base" for step in state.reasoning_trace))
        self.assertTrue(any(step.tool_call and step.tool_call.tool_name == "draft_reply" for step in state.reasoning_trace))

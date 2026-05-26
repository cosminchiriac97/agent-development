import asyncio
import os
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from tools import ToolWrapper
from prompts.registry import PromptRegistry


def react_loop(llm, mesaje: list, max_iterations: int = 5) -> str:
    """React loop: Think → Act → Observe"""
    for _ in range(max_iterations):
        raspuns = llm.invoke(mesaje)
        mesaje.append(raspuns)

        # If LLM no longer requests tools → final response
        if not raspuns.tool_calls:
            content = raspuns.content
            if isinstance(content, list):
                content = "".join(b.get("text", "") for b in content if isinstance(b, dict))
            return content

        # Execute all tools asynchronously
        rezultate = asyncio.run(execute_all_tools(raspuns.tool_calls))
        
        # Add all results to messages
        for rezultat in rezultate:
            mesaje.append({
                "role": "tool",
                "tool_call_id": rezultat["tool_call_id"],
                "content": rezultat["content"]
            })

    raise RuntimeError("Max iterations reached without final response")

# Async tool execution
async def execute_all_tools(tool_calls: list) -> list:
    """Execute all tools concurrently, not sequentially"""
    tasks = [execute_tool_async(tc) for tc in tool_calls]
    return await asyncio.gather(*tasks)

async def execute_tool_async(tool_call: dict) -> dict:
    """Execute a single tool asynchronously"""
    name = tool_call["name"]
    args = tool_call["args"]
    print(f"[Tool Call] '{name}' called with params: {args}")
    try:
        # Run tool in thread pool to avoid blocking
        resultado = await asyncio.to_thread(ToolWrapper.call, name, args)
        return {
            "tool_call_id": tool_call["id"],
            "content": str(resultado)
        }
    except Exception as e:
        return {
            "tool_call_id": tool_call["id"],
            "content": f"Error executing '{name}': {e}"
        }


# ============== TEST: VAT CALCULATOR ==============
def test_vat_calculation():
    """Test: VAT calculation with structured prompt using ReAct Loop"""
    print("\n" + "=" * 70)
    print("TEST: VAT Calculator - Using ReAct Loop")
    print("=" * 70)
    
    # Step 1: Render structured prompt for VAT calculation
    base_amount = "500"
    vat_rate = "19"
    reason = "Electronics purchase"
    
    print(f"\n📋 Step 1: Render VAT Calculation Prompt")
    print("-" * 70)
    prompt_text = registry.render(
        "calculate_expression",
        base_amount=base_amount,
        vat_rate=vat_rate,
        reason=reason
    )
    
    # Step 2: Use ReAct Loop with LLM
    print(f"\n🤖 Step 2: Send to LLM via ReAct Loop")
    print("-" * 70)
    
    if not llm:
        raise RuntimeError("LLM not initialized. Set GOOGLE_API_KEY environment variable.")
    
    messages = [HumanMessage(content=prompt_text)]
    print("Starting ReAct Loop with Gemini AI...")
    response = react_loop(llm, messages)
    print(f"\n✅ Final Response from LLM:\n{response}")
    
    # Step 3: Summary
    print(f"\n✅ Test Summary")
    print("-" * 70)
    print(f"✓ Structured prompt rendered (Identity/Context/Instructions/Constraints/Format Output)")
    print(f"✓ Base Amount: {base_amount} lei")
    print(f"✓ VAT Rate: {vat_rate}%")
    print(f"✓ ReAct Loop executed with tool orchestration")
    print("=" * 70 + "\n")


# ============== TEST: TAX DEDUCTIONS SEARCH ==============
def test_tax_deductions_search():
    """Test: Find tax deductions using ReAct Loop with web search"""
    print("\n" + "=" * 70)
    print("TEST: Tax Deductions Finder - Using ReAct Loop")
    print("=" * 70)
    
    # Step 1: Render structured prompt for tax deduction search
    user_type = "freelancer"
    situation = "home office expenses and equipment"
    country = "Romania"
    
    print(f"\n📋 Step 1: Render Tax Deductions Search Prompt")
    print("-" * 70)
    prompt_text = registry.render(
        "find_tax_deductions",
        user_type=user_type,
        situation=situation,
        country=country
    )
    
    # Step 2: Use ReAct Loop with LLM
    print(f"\n🤖 Step 2: Send to LLM via ReAct Loop")
    print("-" * 70)
    
    if not llm:
        raise RuntimeError("LLM not initialized. Set GOOGLE_API_KEY environment variable.")
    
    messages = [HumanMessage(content=prompt_text)]
    print("Starting ReAct Loop with Gemini AI...")
    response = react_loop(llm, messages)
    print(f"\n✅ Final Response from LLM:\n{response}")
    
    # Step 3: Summary
    print(f"\n✅ Test Summary")
    print("-" * 70)
    print(f"✓ Structured prompt rendered for tax deduction search")
    print(f"✓ User Type: {user_type}")
    print(f"✓ Situation: {situation}")
    print(f"✓ Country: {country}")
    print(f"✓ ReAct Loop executed with web search orchestration")
    print("=" * 70 + "\n")


# ============== TEST: APPOINTMENT REMINDER ==============
def test_appointment_reminder():
    """Test: Create appointment reminder using ReAct Loop with get_datetime"""
    print("\n" + "=" * 70)
    print("TEST: Appointment Reminder - Using ReAct Loop")
    print("=" * 70)
    
    # Step 1: Render structured prompt for appointment reminder
    appointment_type = "Accountant consultation"
    appointment_datetime = "2026-06-15 10:30"
    days_until = "20"
    timezone = "Europe/Bucharest"
    
    print(f"\n📋 Step 1: Render Appointment Reminder Prompt")
    print("-" * 70)
    prompt_text = registry.render(
        "get_appointment_reminder",
        appointment_type=appointment_type,
        appointment_datetime=appointment_datetime,
        days_until=days_until,
        timezone=timezone
    )
    
    # Step 2: Use ReAct Loop with LLM
    print(f"\n🤖 Step 2: Send to LLM via ReAct Loop")
    print("-" * 70)
    
    if not llm:
        raise RuntimeError("LLM not initialized. Set GOOGLE_API_KEY environment variable.")
    
    messages = [HumanMessage(content=prompt_text)]
    print("Starting ReAct Loop with Gemini AI...")
    response = react_loop(llm, messages, 15)
    print(f"\n✅ Final Response from LLM:\n{response}")
    
    # Step 3: Summary
    print(f"\n✅ Test Summary")
    print("-" * 70)
    print(f"✓ Structured prompt rendered for appointment reminder")
    print(f"✓ Appointment: {appointment_type}")
    print(f"✓ Scheduled: {appointment_datetime}")
    print(f"✓ Days until: {days_until}")
    print(f"✓ ReAct Loop executed with datetime orchestration")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    # Initialize LLM (requires GOOGLE_API_KEY environment variable)
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            temperature=0.7,
            timeout=None,
            max_retries=2,
        )
    except Exception as e:
        print(f"LLM initialization failed: {e}")
        print("Set GOOGLE_API_KEY environment variable to use Gemini API")
        llm = None

    if llm:
        llm = llm.bind_tools(ToolWrapper.catalog_gemini())

    # Initialize Prompt Registry
    prompts_folder = Path(__file__).parent / "prompts"
    registry = PromptRegistry(str(prompts_folder))

    # Run all tests
    print("\n" + "🚀 " * 35)
    print("RUNNING ALL PROMPT AND TOOL TESTS")
    print("🚀 " * 35)
    
    # Test 1: Calculator / VAT
    test_vat_calculation()
    
    # Test 2: Web Search / Tax Deductions
    #test_tax_deductions_search()
    
    # Test 3: DateTime / Appointment Reminder
    #test_appointment_reminder()
    
    print("\n" + "✅ " * 35)
    print("ALL TESTS COMPLETED")
    print("✅ " * 35)

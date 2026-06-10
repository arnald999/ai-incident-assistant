from app.services.langfuse_service import langfuse

with langfuse.start_as_current_observation(
    name="langfuse-test",
    as_type="span",
    input={"message": "hello from AI Incident Assistant"},
) as span:
    span.update(output={"status": "ok"})

langfuse.flush()

print("Trace sent")
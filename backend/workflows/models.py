from django.db import models

class Credential(models.Model):
    """
    Stores integration secrets (e.g., API keys, tokens) for external services.
    """
    name = models.CharField(max_length=100, help_text="A name to identify the credential (e.g., 'College ERP API Key')")
    service = models.CharField(max_length=100, help_text="The service this credential is for (e.g., 'ERP', 'Email', 'WhatsApp')")
    # In a real app, we would encrypt the secret key. For now, we store it as plain text (NOT FOR PRODUCTION).
    secret_key = models.TextField(help_text="The secret key or token. WARNING: This is not encrypted in this stub.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.service})"

    class Meta:
        verbose_name_plural = "Credentials"


class Workflow(models.Model):
    """
    Represents a workflow that can be executed.
    """
    TRIGGER_CHOICES = [
        ('schedule', 'Schedule'),
        ('webhook', 'Webhook'),
        ('manual', 'Manual'),
    ]

    name = models.CharField(max_length=200, help_text="A human-readable name for the workflow")
    description = models.TextField(blank=True, help_text="Optional description of the workflow")
    # The natural language request that generated this workflow
    nl_request = models.TextField(help_text="The original natural language request")
    # The structured workflow JSON (as a text field for simplicity)
    workflow_json = models.TextField(help_text="The structured workflow definition in JSON format")
    # Optional: reference to a credential if the workflow needs authentication
    credential = models.ForeignKey(Credential, on_delete=models.SET_NULL, null=True, blank=True, help_text="Credential used for authentication in the workflow")
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_CHOICES, default='manual')
    is_active = models.BooleanField(default=True, help_text="Whether the workflow is active and can be triggered")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

from django.db import models
from django.utils import timezone
from .services.credentials.vault import credential_vault
import json

class Credential(models.Model):
    """
    Stores integration secrets (e.g., API keys, tokens) for external services.
    The actual secret is stored encrypted in the vault, and only the reference is kept here.
    """
    name = models.CharField(max_length=100, help_text="A name to identify the credential (e.g., 'College ERP API Key')")
    service = models.CharField(max_length=100, help_text="The service this credential is for (e.g., 'ERP', 'Email', 'WhatsApp')")
    # We store a reference to the encrypted credential in the vault
    # In a real implementation, this might be a database reference or vault path
    credential_reference = models.CharField(max_length=255, blank=True, null=True, 
                                          help_text="Reference to the encrypted credential in the vault")
    # For backward compatibility and simplicity in this demo, we'll also keep an encrypted version
    # In production, you would NOT store encrypted credentials in the model directly
    encrypted_secret_key = models.TextField(blank=True, null=True,
                                          help_text="Encrypted secret key (for demo purposes)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.service})"

    def set_secret_key(self, secret_key):
        """
        Set the secret key for this credential, encrypting it for storage.
        """
        if secret_key:
            # Encrypt the secret key
            encrypted = credential_vault.encrypt_credential(secret_key)
            self.encrypted_secret_key = encrypted
            # In a real implementation, you would store this in a secure vault
            # and only keep a reference here
            self.credential_reference = f"cred_{self.id if self.id else 'new'}_{int(timezone.now().timestamp())}"
        else:
            self.encrypted_secret_key = None
            self.credential_reference = None

    def get_secret_key(self):
        """
        Get the decrypted secret key for this credential.
        Returns None if no secret is set.
        """
        if not self.encrypted_secret_key:
            return None
        
        try:
            return credential_vault.decrypt_credential(self.encrypted_secret_key)
        except Exception as e:
            # Log the error in production
            return None

    def is_encrypted(self):
        """
        Check if the credential has an encrypted secret.
        """
        return bool(self.encrypted_secret_key)

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
    credential = models.ForeignKey(Credential, on_delete=models.SET_NULL, null=True, blank=True, 
                                 help_text="Credential used for authentication in the workflow")
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_CHOICES, default='manual')
    is_active = models.BooleanField(default=True, help_text="Whether the workflow is active and can be triggered")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

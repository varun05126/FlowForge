from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Workflow, Credential
from .services.nl_parser import nl_parser_service
from .services.execution_engine import execution_engine_service
from .services.credentials.vault import credential_vault
import json

class ParseWorkflowView(APIView):
    """
    POST /api/workflows/parse
    Accepts NL text, returns structured workflow JSON
    """
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            nl_text = request.data.get('text', '')
            if not nl_text:
                return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Use the NL parser service to get structured workflow
            workflow_data = nl_parser_service.parse(nl_text)
            
            # In a real app, we might save the workflow here, but the endpoint is just for parsing
            return Response(workflow_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkflowListCreateView(APIView):
    """
    GET /api/workflows -> list workflows
    POST /api/workflows -> save a workflow
    """
    def get(self, request):
        workflows = Workflow.objects.all().values()
        return Response(list(workflows))
    
    def post(self, request):
        try:
            # Handle credential encryption if present
            credential_id = None
            if request.data.get('credential_data'):
                # Encrypt and store the credential data
                credential_data = request.data['credential_data']
                credential_name = request.data.get('credential_name', 'Unnamed Credential')
                credential_service = request.data.get('credential_service', 'Unknown')
                
                # Create or get the credential record
                credential, created = Credential.objects.get_or_create(
                    name=credential_name,
                    service=credential_service,
                    defaults={}
                )
                
                # Encrypt and store the credential data
                credential.set_secret_key(credential_data)
                credential.save()
                
                credential_id = credential.id
            
            # Create a new workflow
            workflow = Workflow.objects.create(
                name=request.data.get('name', 'Unnamed Workflow'),
                description=request.data.get('description', ''),
                nl_request=request.data.get('nl_request', ''),
                workflow_json=json.dumps(request.data.get('workflow_json', {})),
                credential_id=credential_id,
                trigger_type=request.data.get('trigger_type', 'manual'),
                is_active=request.data.get('is_active', True)
            )
            return Response({'id': workflow.id, 'message': 'Workflow created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkflowDetailView(APIView):
    """
    GET /api/workflows/:id -> get one workflow
    """
    def get(self, request, workflow_id):
        try:
            workflow = Workflow.objects.get(id=workflow_id)
            # Get decrypted credential if needed (be careful about exposing secrets!)
            credential_dict = None
            if workflow.credential and workflow.credential.is_encrypted():
                # In a real API, you would NOT return the decrypted credential
                # This is only for demonstration purposes in this controlled environment
                decrypted_secret = workflow.credential.get_secret_key()
                if decrypted_secret is not None:
                    credential_dict = {
                        'id': workflow.credential.id,
                        'name': workflow.credential.name,
                        'service': workflow.credential.service,
                        # Note: In a real API, you would not return the actual secret
                        # 'secret_key': decrypted_secret,  # NEVER DO THIS IN PRODUCTION
                        'has_secret': True
                    }
                else:
                    credential_dict = {
                        'id': workflow.credential.id,
                        'name': workflow.credential.name,
                        'service': workflow.credential.service,
                        'has_secret': False
                    }
            elif workflow.credential:
                credential_dict = {
                    'id': workflow.credential.id,
                    'name': workflow.credential.name,
                    'service': workflow.credential.service,
                    'has_secret': False
                }
            
            response_data = {
                'id': workflow.id,
                'name': workflow.name,
                'description': workflow.description,
                'nl_request': workflow.nl_request,
                'workflow_json': json.loads(workflow.workflow_json),
                'credential': credential_dict,
                'trigger_type': workflow.trigger_type,
                'is_active': workflow.is_active,
                'created_at': workflow.created_at,
                'updated_at': workflow.updated_at
            }
            return Response(response_data)
        except Workflow.DoesNotExist:
            return Response({'error': 'Workflow not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkflowRunView(APIView):
    """
    POST /api/workflows/:id/run -> trigger manual execution (stubbed)
    """
    def post(self, request, workflow_id):
        try:
            # Run the workflow using the execution engine service
            result = execution_engine_service.run_workflow(workflow_id)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Additional credential management endpoints
class CredentialListCreateView(APIView):
    """
    GET /api/credentials -> list credentials (without secrets)
    POST /api/credentials -> create a new credential
    """
    def get(self, request):
        credentials = Credential.objects.all().values(
            'id', 'name', 'service', 'created_at', 'updated_at'
        )
        # Add a flag indicating if the credential has a secret
        credential_list = []
        for cred in credentials:
            cred_obj = Credential.objects.get(id=cred['id'])
            cred['has_secret'] = cred_obj.is_encrypted()
            credential_list.append(cred)
        return Response(credential_list)
    
    def post(self, request):
        try:
            name = request.data.get('name')
            service = request.data.get('service')
            secret_key = request.data.get('secret_key')
            
            if not name or not service:
                return Response({'error': 'Name and service are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create or get the credential
            credential, created = Credential.objects.get_or_create(
                name=name,
                service=service,
                defaults={}
            )
            
            if secret_key is not None:
                credential.set_secret_key(secret_key)
            
            credential.save()
            
            return Response({
                'id': credential.id,
                'message': 'Credential created successfully' if created else 'Credential updated successfully'
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CredentialDetailView(APIView):
    """
    GET /api/credentials/:id -> get a credential (without secret)
    PUT /api/credentials/:id -> update a credential
    DELETE /api/credentials/:id -> delete a credential
    """
    def get(self, request, credential_id):
        try:
            credential = Credential.objects.get(id=credential_id)
            return Response({
                'id': credential.id,
                'name': credential.name,
                'service': credential.service,
                'has_secret': credential.is_encrypted(),
                'created_at': credential.created_at,
                'updated_at': credential.updated_at
            })
        except Credential.DoesNotExist:
            return Response({'error': 'Credential not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, credential_id):
        try:
            credential = Credential.objects.get(id=credential_id)
            data = request.data
            
            if 'name' in data:
                credential.name = data['name']
            if 'service' in data:
                credential.service = data['service']
            if 'secret_key' in data:
                credential.set_secret_key(data['secret_key'])
            
            credential.save()
            
            return Response({'message': 'Credential updated successfully'})
        except Credential.DoesNotExist:
            return Response({'error': 'Credential not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, credential_id):
        try:
            credential = Credential.objects.get(id=credential_id)
            credential.delete()
            return Response({'message': 'Credential deleted successfully'})
        except Credential.DoesNotExist:
            return Response({'error': 'Credential not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

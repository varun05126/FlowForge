from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Workflow, Credential
from .services.nl_parser import nl_parser_service
from .services.execution_engine import execution_engine_service

@method_decorator(csrf_exempt, name='dispatch')
class ParseWorkflowView(View):
    """
    POST /api/workflows/parse
    Accepts NL text, returns structured workflow JSON (stubbed)
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
            nl_text = data.get('text', '')
            if not nl_text:
                return JsonResponse({'error': 'Text is required'}, status=400)
            
            # Use the NL parser service to get structured workflow
            workflow_data = nl_parser_service.parse(nl_text)
            
            # In a real app, we might save the workflow here, but the endpoint is just for parsing
            return JsonResponse(workflow_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class WorkflowListCreateView(View):
    """
    GET /api/workflows -> list workflows
    POST /api/workflows -> save a workflow
    """
    def get(self, request):
        workflows = Workflow.objects.all().values()
        return JsonResponse(list(workflows), safe=False)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            # Create a new workflow
            workflow = Workflow.objects.create(
                name=data.get('name', 'Unnamed Workflow'),
                description=data.get('description', ''),
                nl_request=data.get('nl_request', ''),
                workflow_json=json.dumps(data.get('workflow_json', {})),
                credential_id=data.get('credential_id'),
                trigger_type=data.get('trigger_type', 'manual'),
                is_active=data.get('is_active', True)
            )
            return JsonResponse({'id': workflow.id, 'message': 'Workflow created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class WorkflowDetailView(View):
    """
    GET /api/workflows/:id -> get one workflow
    """
    def get(self, request, workflow_id):
        try:
            workflow = Workflow.objects.get(id=workflow_id)
            return JsonResponse({
                'id': workflow.id,
                'name': workflow.name,
                'description': workflow.description,
                'nl_request': workflow.nl_request,
                'workflow_json': json.loads(workflow.workflow_json),
                'credential_id': workflow.credential_id,
                'trigger_type': workflow.trigger_type,
                'is_active': workflow.is_active,
                'created_at': workflow.created_at,
                'updated_at': workflow.updated_at
            })
        except Workflow.DoesNotExist:
            return JsonResponse({'error': 'Workflow not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class WorkflowRunView(View):
    """
    POST /api/workflows/:id/run -> trigger manual execution (stub)
    """
    def post(self, request, workflow_id):
        try:
            # Run the workflow using the execution engine service
            result = execution_engine_service.run_workflow(workflow_id)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

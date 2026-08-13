import json
import time
import uuid
from datetime import datetime, timedelta
from ..models import Workflow
import logging

logger = logging.getLogger(__name__)

class ExecutionEngineService:
    """
    Workflow Execution Engine service.
    In a real implementation, this would fetch data from sources, 
    process it, and deliver the output (e.g., send an email, store in a database, etc.).
    This implementation simulates execution with realistic delays and mock data.
    """
    
    def __init__(self):
        # In-memory storage for execution history (in production, use a database or file)
        self.execution_history = []
    
    def run_workflow(self, workflow_id):
        """
        Run a workflow by its ID.
        This simulates workflow execution with realistic steps.
        
        Args:
            workflow_id (int): The ID of the workflow to run.
            
        Returns:
            dict: A dictionary representing the execution result.
        """
        start_time = time.time()
        execution_id = str(uuid.uuid4())
        
        try:
            # Get the workflow from database
            workflow = Workflow.objects.get(id=workflow_id)
            logger.info(f"Starting execution of workflow {workflow.id}: {workflow.name}")
            
            # Parse the workflow JSON
            try:
                workflow_json = json.loads(workflow.workflow_json)
            except json.JSONDecodeError:
                workflow_json = {}
            
            # Simulate execution steps
            execution_steps = self._get_execution_steps(workflow_json)
            
            # Execute each step
            step_results = []
            for i, step in enumerate(execution_steps):
                logger.info(f"Executing step {i+1}/{len(execution_steps)}: {step['description']}")
                
                # Simulate processing time
                time.sleep(0.5)  # 500ms delay per step for realism
                
                # Execute the step
                step_result = self._execute_step(step, workflow_json, i+1)
                step_results.append(step_result)
                
                # If a step fails, stop execution (unless it's marked as continue_on_failure)
                if not step_result.get('success', False) and not step.get('continue_on_failure', False):
                    logger.warning(f"Step {i+1} failed, stopping execution")
                    break
            
            # Determine overall success
            all_successful = all(step.get('success', False) for step in step_results)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Create execution result
            result = {
                "execution_id": execution_id,
                "workflow_id": workflow.id,
                "workflow_name": workflow.name,
                "status": "completed" if all_successful else "failed",
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "end_time": datetime.fromtimestamp(time.time()).isoformat(),
                "duration_seconds": round(duration, 2),
                "steps_executed": len(step_results),
                "total_steps": len(execution_steps),
                "step_results": step_results,
                "output": self._generate_output(step_results, workflow_json),
                "logs": [f"Workflow execution {execution_id} completed with status: {'completed' if all_successful else 'failed'}"]
            }
            
            # Store in execution history (limit to last 100 executions)
            self.execution_history.append(result)
            if len(self.execution_history) > 100:
                self.execution_history = self.execution_history[-100:]
            
            logger.info(f"Workflow execution completed: {result['status']} in {duration:.2f}s")
            return result
            
        except Workflow.DoesNotExist:
            logger.error(f"Workflow with ID {workflow_id} not found")
            return {
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "status": "failed",
                "error": "Workflow not found",
                "logs": [f"Execution failed: Workflow with ID {workflow_id} not found"]
            }
        except Exception as e:
            logger.error(f"Error executing workflow {workflow_id}: {str(e)}", exc_info=True)
            return {
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(execution_id),
                "logs": [f"Execution failed due to error: {str(e)}"]
            }
    
    def _get_execution_steps(self, workflow_json):
        """
        Determine the execution steps based on the workflow JSON.
        In a real implementation, this would be more sophisticated.
        """
        steps = []
        
        # Extract information from workflow JSON
        trigger = workflow_json.get('trigger', '').lower()
        source = workflow_json.get('source', '').lower()
        action = workflow_json.get('action', '').lower()
        details = workflow_json.get('details', '')
        
        # Step 1: Validate input
        steps.append({
            "id": "validate_input",
            "description": "Validate workflow input and parameters",
            "continue_on_failure": False
        })
        
        # Step 2: Connect to source (if applicable)
        if source and source != "unknown":
            steps.append({
                "id": "connect_source",
                "description": f"Connect to {source} source",
                "continue_on_failure": True  # Can sometimes proceed with cached data
            })
        
        # Step 3: Extract/fetch data
        steps.append({
            "id": "fetch_data",
            "description": "Fetch data from source",
            "continue_on_failure": False
        })
        
        # Step 4: Process data
        steps.append({
            "id": "process_data",
            "description": "Process and transform data",
            "continue_on_failure": False
        })
        
        # Step 5: Perform action
        if action and action != "unknown":
            steps.append({
                "id": "perform_action",
                "description": f"Perform {action} action",
                "continue_on_failure": False
            })
        
        # Step 6: Save results
        steps.append({
            "id": "save_results",
            "description": "Save execution results",
            "continue_on_failure": True
        })
        
        # Step 7: Send notifications
        steps.append({
            "id": "send_notifications",
            "description": "Send completion notifications",
            "continue_on_failure": True
        })
        
        return steps
    
    def _execute_step(self, step, workflow_json, step_number):
        """
        Execute a single step of the workflow.
        """
        step_id = step["id"]
        
        try:
            # Simulate different types of steps
            if step_id == "validate_input":
                # Always succeed for validation in this simulation
                return {
                    "step": step_number,
                    "id": step_id,
                    "description": step["description"],
                    "success": True,
                    "output": "Input validation passed",
                    "timestamp": datetime.now().isoformat()
                }
            
            elif step_id == "connect_source":
                source = workflow_json.get('source', 'Unknown')
                # Simulate connection success/failure (90% success rate)
                import random
                success = random.random() > 0.1
                return {
                    "step": step_number,
                    "id": step_id,
                    "description": step["description"],
                    "success": success,
                    "output": f"Connected to {source} source" if success else f"Failed to connect to {source} source",
                    "timestamp": datetime.now().isoformat()
                }
            
            elif step_id == "fetch_data":
                # Simulate fetching data
                details = workflow_json.get('details', '')
                # Extract potential data size from details
                data_size = "1KB"  # Default
                size_match = re.search(r'(\d+)\s*(kb|mb|gb)', details, re.IGNORECASE)
                if size_match:
                    data_size = f"{size_match.group(1)}{size_match.group(2).upper()}"
                
                return {
                    "step": step_number,
                    "id": step_id,
                    "description": step["description"],
                    "success": True,
                    "output": f"Fetched {data_size} of data",
                    "data_size": data_size,
                    "timestamp": datetime.now().isoformat()
                }
            
            elif step_id == "process_data":
                # Simulate data processing
                action = workflow_json.get('action', 'process')
                processing_time = 0.3  # Simulated processing time
                time.sleep(processing_time)
                
                return {
                    "step": step_number,
                    "id": step_id,
                    "description": step["description"],
                    "success": True,
                    "output": f"Data processed using {action} operation",
                    "processing_time_ms": int(processing_time * 1000),
                    "timestamp": datetime.now().isoformat()
                }
            
            elif step_id == "perform_action":
                action = workflow_json.get('action', 'unknown').lower()
                # Simulate different actions
                if 'email' in action or 'notify' in action:
                    return {
                        "step": step_number,
                        "id": step_id,
                        "description": step["description"],
                        "success": True,
                        "output": "Notification sent successfully",
                        "notification_id": str(uuid.uuid4())[:8],
                        "timestamp": datetime.now().isoformat()
                    }
                elif 'file' in action or 'save' in action:
                    return {
                        "step": step_number,
                        "id": step_id,
                        "description": step["description"],
                        "success": True,
                        "output": "File saved successfully",
                        "file_path": f"/tmp/workflow_output_{int(time.time())}.dat",
                        "timestamp": datetime.now().isoformat()
                    }
                elif 'database' in action or 'store' in action:
                    return {
                        "step": step_number,
                        "id": step_id,
                        "description": step["description"],
                        "success": True,
                        "output": "Data stored in database successfully",
                        "records_affected": 42,  # Mock value
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "step": step_number,
                        "id": step_id,
                        "description": step["description"],
                        "success": True,
                        "output": f"Action '{action}' completed",
                        "timestamp": datetime.now().isoformat()
                    }
            
            elif step_id == "save_results":
                return {
                    "step": step_number,
                    "id": step_id,
                    "description": step["description"],
                    "success": True,
                    "output": "Results saved to execution history",
                    "timestamp": datetime.now().isoformat()
                }
            
            elif step_id == "send_notifications":
                # Simulate notification sending (95% success rate)
                import random
                success = random.random() > 0.05
                return {
                    "step": step_number,
                    "id": step_id,
                    "description": step["description"],
                    "success": success,
                    "output": "Notifications sent" if success else "Failed to send some notifications",
                    "timestamp": datetime.now().isoformat()
                }
            
            else:
                # Generic step
                return {
                    "step": step_number,
                    "id": step_id,
                    "description": step["description"],
                    "success": True,
                    "output": "Step completed",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error in step {step_id}: {str(e)}", exc_info=True)
            return {
                "step": step_number,
                "id": step_id,
                "description": step["description"],
                "success": False,
                "error": str(e),
                "output": f"Step failed due to error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_output(self, step_results, workflow_json):
        """
        Generate a summary output from the step results.
        """
        successful_steps = [s for s in step_results if s.get('success', False)]
        failed_steps = [s for s in step_results if not s.get('success', False)]
        
        output_parts = [
            f"Workflow executed successfully with {len(successful_steps)}/{len(step_results)} steps completed."
        ]
        
        if failed_steps:
            output_parts.append(f"{len(failed_steps)} steps failed: {', '.join([s['id'] for s in failed_steps])}")
        
        # Add specific outputs from steps
        for step in successful_steps:
            if 'output' in step and step['output']:
                output_parts.append(f"- {step['output']}")
        
        return " | ".join(output_parts)
    
    def get_execution_history(self, workflow_id=None, limit=10):
        """
        Get execution history, optionally filtered by workflow ID.
        """
        history = self.execution_history
        if workflow_id is not None:
            history = [ex for ex in history if ex.get('workflow_id') == workflow_id]
        return sorted(history, key=lambda x: x.get('start_time', ''), reverse=True)[:limit]

# Create a singleton instance for easy access
execution_engine_service = ExecutionEngineService()

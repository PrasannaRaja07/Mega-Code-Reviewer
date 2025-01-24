from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
import os
import glob

load_dotenv()
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})
print(os.getenv("MIRA_API_KEY"))

def deploy_flows():
    flow_files = glob.glob("flows/*.yaml")
    if not flow_files:
        print("No flow files found in the 'flows' directory.")
        return

    for flow_file in flow_files:
        try:
            flow = Flow(source=flow_file)
            response = client.flow.deploy(flow)
            if response.get("status") == "success":
                flow_name = os.path.splitext(os.path.basename(flow_file))[0]
                flow_id = f"prasannaraja07/{flow_name}"
                print(f"Flow deployed successfully with ID: {flow_id}")
            else:
                print(f"Flow deployment failed for {flow_file}: {response}")
        except FlowError as e:
            print(f"Error deploying flow {flow_file}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error with {flow_file}: {str(e)}")

def test_flow(flow_id, inputs):
    try:
        result = client.flow.execute(flow_id, inputs)
        return result
    except FlowError as e:
        print(f"Error running flow: {str(e)}")
    except Exception as e:
        print(f"Unexpected error during flow execution: {str(e)}")
    return None

def main():
    print("Deploying flows...")
    deploy_flows()

    print("\nTesting code-reviewer flow...")
    code_sample = """
    def add(a, b):
        return a + b  # No type hints or error handling
    """
    flow_id = "prasannaraja07/code-reviewer"
    result = test_flow(flow_id, {
        "code": code_sample,
        "language": "python"
    })

    if result:
        print("\nCode Review Results:")
        print(result)
    else:
        print("Flow execution failed.")

if __name__ == "__main__":
    main()

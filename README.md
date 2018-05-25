Lambda functions to terminate new ec2 instances which fail their respective security checks.
1) Name tag cannot be empty.
2) Security group cannot be default.
3) SSH cannot be open to the world.

Trigger lambda functions from a cloudwatch event of ec2 state "running".

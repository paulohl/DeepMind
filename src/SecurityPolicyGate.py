import math

class AdvancedSecurityPolicyGate:
    """
    Enforces non-probabilistic Lipschitz error bounds and state-invariant
    safeties on incoming model predictions to maintain stability.
    """
    def __init__(self, restricted_actions, max_permissible_drift=0.15):
        self.forbidden_actions = restricted_actions
        self.epsilon = max_permissible_drift

    def verify_lipschitz_bound(self, base_latent, inference_latent) -> bool:
        """
        Verifies the system transition does not violate:
        || f(x; W) - f(x; W_q) || <= epsilon
        """
        # Calculate Euclidean distance metric between expected and empirical vectors
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(base_latent, inference_latent)))
        return distance <= self.epsilon

    def validate(self, control_action: dict, latent_states: tuple = None) -> bool:
        # 1. Categorical Boundary Invalidation
        action_type = control_action.get("action", "")
        if action_type in self.forbidden_actions:
            return False

        # 2. Structural Constraint: Target Allocation Verified
        if "target_resource" not in control_action:
            return False

        # 3. Numerical Substrate Drift Verification (If Latent Vectors Provided)
        if latent_states:
            base, empirical = latent_states
            if not self.verify_lipschitz_bound(base, empirical):
                return False

        return True

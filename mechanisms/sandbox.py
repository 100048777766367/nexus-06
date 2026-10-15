from mechanisms.base import BaseMechanism

class SandboxMechanism(BaseMechanism):
    name = "sandbox"
    priority = 31  # Chạy ngay sau phán quyết Siêu XOR

    def simulate_future(self, decision, candidate_action):
        pain_risk = abs(decision - 0.5) * candidate_action
        stability_score = 1.0 - abs(decision - 0.5)
        loss_estimate = round((pain_risk * 0.6) + ((1.0 - stability_score) * 0.4), 4)
        return loss_estimate

    def execute(self, context):
        raw_decision = context.get("final_decision", 0.5)
        print(f"🔮 [MENTAL SANDBOX] Đưa phán quyết thô ({raw_decision}) vào phòng giả lập tâm thức...")

        variations = [0.85, 0.95, 1.0, 1.05, 1.15]
        simulation_results = []

        for factor in variations:
            test_decision = max(0.01, min(0.99, round(raw_decision * factor, 4)))
            loss = self.simulate_future(test_decision, factor)
            simulation_results.append((loss, test_decision))

        simulation_results.sort(key=lambda x: x[0])
        best_loss, optimal_decision = simulation_results[0]

        print(f"✨ [GIẢ LẬP TỐI ƯU] Đã thử 5 tương lai. Chọn kịch bản tổn hại thấp nhất: Loss={best_loss} ──► Điều biến: {optimal_decision}")
        context["final_decision"] = optimal_decision
        context["sandbox_simulation"] = {
            "tested_futures": len(variations),
            "lowest_loss": best_loss,
            "optimal_adjusted_decision": optimal_decision
        }

from pydantic import BaseModel

class HardwareSuggestion(BaseModel):
    suggested_hardware: str
    reasoning: str

def recommend_for_algorithm(algorithm: str) -> HardwareSuggestion:
    algo_lower = algorithm.lower()

    if "fft" in algo_lower:
        return HardwareSuggestion(
            suggested_hardware="GPU-accelerated backend (e.g., NVIDIA A100)",
            reasoning="FFT is highly parallelizable; GPUs generally outperform CPUs. Quantum FFT hardware not yet practical for typical workloads."
        )
    elif "dijkstra" in algo_lower or "shortest path" in algo_lower:
        return HardwareSuggestion(
            suggested_hardware="CPU cluster (multi-core) with large memory",
            reasoning="Graph algorithms like Dijkstra benefit from fast memory and good single-thread performance; quantum advantage is unclear."
        )
    else:
        return HardwareSuggestion(
            suggested_hardware="Classical CPU/GPU (depends on workload)",
            reasoning="No specific quantum advantage identified. Placeholder for RAG-enhanced logic."
        )

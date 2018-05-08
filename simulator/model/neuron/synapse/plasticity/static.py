from simulator.model.neuron.synapse.plasticity.plasticity_model import PlasticityModel


class StaticPlasticityModel(PlasticityModel):
    def __init__(self):
        PlasticityModel.__init__(self)

    def apply_spike(self, timing) -> float:
        return 1.0

    def apply_action_potential(self, timing, force=1.0):
        return

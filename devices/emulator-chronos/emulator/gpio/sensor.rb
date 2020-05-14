class Emulator::GPIO::Sensor < Emulator::GPIO::Base
  direction :input

  def update state
    value = state["value"].to_i
    return if value < @state["min"].to_i
    return if value > @state["max"].to_i

    @state["value"] = value
  end
end

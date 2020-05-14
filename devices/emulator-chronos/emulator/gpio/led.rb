class Emulator::GPIO::Led < Emulator::GPIO::Base
  direction :output

  def update state
    return unless is_bool?(state["on"])
    @state["on"] = state["on"]
  end
end

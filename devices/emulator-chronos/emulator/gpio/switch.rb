class Emulator::GPIO::Switch < Emulator::GPIO::Base
  direction :input

  def update state
    return unless is_bool?(state["open"])
    @state["open"] = state["open"]
  end
end

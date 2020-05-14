module Emulator::GPIO
  def self.for_type(type, id, params = {})
    klass = type.capitalize.to_sym
    Emulator::GPIO.const_get(klass).new(id, params)
  end
  
  require "./emulator/gpio/base"
  require "./emulator/gpio/led"
  require "./emulator/gpio/sensor"
  require "./emulator/gpio/switch"
end

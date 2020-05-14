class Emulator::Device
  attr_accessor :name, :gpios

  def initialize
    config = Emulator.config.data
    @name = config["name"]

    create_gpios(config["gpios"])
  end
  
  def to_json
    {
      name: @name,
      gpios: gpios_to_json
    }
  end
  
  def gpios_to_json
    @gpios.map { |id, gpio| [id, gpio.to_json] }.to_h
  end

  private
  def create_gpios gpios
    @gpios = gpios.map do |id, config|
      [id, Emulator::GPIO.for_type(config["type"], id, config)]
    end.to_h
  end
end

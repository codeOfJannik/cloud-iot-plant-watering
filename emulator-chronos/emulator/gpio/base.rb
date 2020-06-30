class Emulator::GPIO::Base
  attr_accessor :id, :type, :direction, :state

  def initialize id, params = {}
    @id = id
    @type = self.class.name.split('::').last.downcase
    @state = params["state"]
    @direction = self.class.instance_variable_get(:@direction)
    validate!
  end

  def validate!
    raise "missing id" unless @id
    raise "invalid direction" unless DIRECTIONS.include?(@direction)
  end

  def update state
  end

  def is_bool?(x)
    [true, false].include?(x)
  end

  DIRECTIONS = [:input, :output].freeze
  def self.direction direction
    @direction = direction
  end

  def to_json
    {
      id: @id,
      type: @type,
      direction: @direction,
      state: @state
    }
  end
end

ENV['RACK_ENV'] = 'test'
require 'minitest/autorun'
require 'rack/test'

require './emulator.rb'

module EmulatorTest
end

class EmulatorTest::Test < Minitest::Test
  include Rack::Test::Methods

  def app
    Emulator::Server
  end
end


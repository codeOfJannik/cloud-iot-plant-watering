require "./tests/test_helper"

class EmulatorTest::Config < EmulatorTest::Test
  def test_parse
    config = Emulator::Config.new
    assert_equal "/emulator/config.yaml", config.file
    assert_equal "Test Device", config.data["name"]
  end
end

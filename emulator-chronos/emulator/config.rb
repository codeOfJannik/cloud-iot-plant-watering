require 'yaml'

class Emulator::Config
  attr_accessor :file, :templates, :assets, :data

  def initialize
    @file = "#{Dir.pwd}/config.yaml"
    @templates = "#{Dir.pwd}/templates"
    @assets = "#{Dir.pwd}/assets"
    @data = YAML.load_file(@file)
  end
end

require 'bundler/setup'
require 'sinatra'

module Emulator
  def self.config
    @config ||= Config.new
  end
  
  def self.device
    @device ||= Device.new
  end

  require "./emulator/config"
  require "./emulator/device"
  require "./emulator/gpio"
  require "./emulator/server"
end

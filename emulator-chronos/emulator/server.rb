require 'sinatra/base'
require 'sinatra/json'
require 'sinatra/reloader'

class Emulator::Server < Sinatra::Base
  configure :development do
    register Sinatra::Reloader
  end
  set :views, Emulator.config.templates
  set :public_folder, Emulator.config.assets

  get "/" do
    @device = Emulator.device
    @gpios = @device.gpios
    erb :index
  end
  
  get "/device" do
    @device = Emulator.device
    halt(404) if @device.nil?

    json @device.to_json
  end
  
  get "/gpios" do
    @device = Emulator.device
    halt(404) if @device.nil?

    json @device.gpios_to_json
  end

  get "/gpios/:id" do
    @gpio = Emulator.device.gpios[params["id"]]
    halt(404) if @gpio.nil?

    json @gpio.to_json
  end
  
  post "/gpios/:id" do
    @gpio = Emulator.device.gpios[params["id"]]
    halt(404) if @gpio.nil?

    status = JSON.parse(request.body.read)
    @gpio.update(status)

    json @gpio.to_json
  end
end

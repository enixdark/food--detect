require 'rest-client'

class ImagesController < ApplicationController
  
  def index
    @image = Image.new
  end

  def create
    @image = Image.new(image_params)
    respond_to do |format|
      if @image.save
        # RestClient.post "http://localhost:5000/path", 
        #   {
        #     'file' => "#{ImageUploader.class_variable_get(:@@static_store)}/#{image_params['file'].original_filename}",
        #     'client_id' => params.require(:client_id)  
        #   }.to_json, 
        #     {content_type: :json, accept: :json}
        format.js
      end
    end
  end

  private
    def image_params
      params.require(:image).permit(:file)
    end
end

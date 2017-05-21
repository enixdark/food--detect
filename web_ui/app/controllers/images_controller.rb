require 'rest-client'

class ImagesController < ApplicationController
  
  def index
    @image = Image.new
  end

  def create
    @image = Image.new(image_params)
    respond_to do |format|
      if @image.save
        RestClient.post ( ENV['IMAGE_SERVICE_URI'] || "http://localhost:5000/path" ), 
          {
            'file' => "#{ImageUploader.class_variable_get(:@@static_store)}/#{image_params['file'].original_filename}",
            'client_id' => params.require(:client_id)  
          }.to_json, 
            {content_type: :json, accept: :json}
        format.js
      end
    end
  end

  def return_data
    name = {
      :buncha => 'Bún chả',
      :comrang => 'Cơm rang',
      :pho => 'Phở',
      :banhmi => 'Bánh mỳ'
    }
    @video_data = JSON.parse ( (JSON.parse params[:video_data_params] )["context"] )
    param_name = (JSON.parse params[:video_data_params] )["name"] 

    @food_name = name[param_name.to_sym]

    
    httpRequestUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?location=21.0037751%2C105.84767509999999&radius=1000&sensor=true&query="cửa%20hàng%20' + @food_name + '"&key=AIzaSyCxW4mgsZ9R4JYD4rMw6qu9F5bFwMqAsLQ'
    require 'net/http'
    
    result_data = JSON.parse( Net::HTTP.get(URI.parse(httpRequestUrl)) )


    curl -H "Content-Type: application/json" --data @body.json http://localhost:8080/ui/webapp/conf

    respond_to do |format|
      format.js
    end
  end

  private
    def image_params
      params.require(:image).permit(:file)
    end
end

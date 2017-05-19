class ImagesController < ApplicationController
  def index
    @image = Image.new
  end

  def create
    @image = Image.new(image_params)

    if @image.save 
      respond_to do |format|
        format.js { render 'create' }
      end
    else
      respond_to do |format|
        format.js { render 'create' }
      end
    end
  end

  private
    def image_params
      params.require(:image).permit(:file)
    end
end

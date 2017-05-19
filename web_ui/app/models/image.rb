class Image < ApplicationRecord
  mount_uploader :file, ImageUploader

  validates_processing_of :file
  validate :image_size_validation
 
  private
  
  def image_size_validation
    errors[:file] << "Should be less than 5MB" if file.size > 5.megabytes
  end
end

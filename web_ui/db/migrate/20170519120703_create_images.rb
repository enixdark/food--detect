class CreateImages < ActiveRecord::Migration[5.0]
  def change
    create_table :images do |t|
      t.string  :name
      t.string  :size
      t.text    :suggest 
      t.string  :path

      t.timestamps
    end
  end
end

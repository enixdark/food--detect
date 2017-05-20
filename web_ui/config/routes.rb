Rails.application.routes.draw do
  root 'images#index'
  resources :images, only: :create, defaults: { format: 'js' }
  namespace :images do
    post 'return_data'
  end
end

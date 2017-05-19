Rails.application.routes.draw do
  root 'images#index'
  resources :images, only: :create, defaults: { format: 'js' }
end

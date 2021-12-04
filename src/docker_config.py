import os

project_dir = os.getcwd()

docker_image = 'mooswell/custom-chromium:ver1'
docker_user = 'pptruser'
docker_container_home = '/home/pptruser/'
docker_shared_dir_root = project_dir
vols = { 
	docker_shared_dir_root + '/app': {
		'bind': docker_container_home + 'app',
		'mode':'rw'
	}	
}

permission_collection_script   = 'capture_permission_requests.js'
notification_collection_script = 'capture_notifications.js'

CRAWL_MAX_CONTAINERS = 3
CRAWL_TIMEOUT = 180
ANALYSIS_MAX_CONTAINERS = 20
ANALYSIS_TIMEOUT = 1000

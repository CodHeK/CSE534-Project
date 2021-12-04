import docker
import os
import time
import datetime
import logging
import tarfile
import traceback

from docker_config import *

client = docker.from_env()


logging.basicConfig(filename='output2.log', filemode='w', format='%(name)s - %(funcName)20s() - %(message)s',level=logging.INFO)
export_path = './containers_data/container_'

def get_time():
	currentDT = datetime.datetime.now()
	return '['+currentDT.strftime("%Y-%m-%d %H:%M:%S") +'] '


def initiate_container(url, id, script_name, iteration_count,  container_timeout):	
    try:
        ## create and setup container ##
        logging.info(get_time() + 'container_'+id+' creating!!')
        container_id  = client.containers.create(image=docker_image,name='container_'+id,volumes = vols,
                                                shm_size='1G', user=docker_user, 
                                                publish_all_ports=True, detach=False)
        container = client.containers.get('container_'+str(id))
        container.start()
        logging.info(get_time() + 'container_'+id+' created successfully!!')    
        
        ## wait for display to be activated ##
        time.sleep(10)
        ## Exeecute the browser automation script
        execute_script(url, id, script_name,  iteration_count, container_timeout-100)
    except Exception as e:
        logging.info(e) 


def execute_script(url, id, script_name,  iteration_count, container_timeout):
    try:	
        ## Execute javascript file
        logging.info(get_time() +'container_'+id+': Executing javascript')
        container = client.containers.get('container_'+str(id))               
        #logs = container.attach(stream=True,stdout=True,stderr=True)
        _,logs = container.exec_run(cmd=['node',script_name,url,id,str(iteration_count),str(container_timeout)], user=docker_user, detach=False, stream=True)
        time.sleep(container_timeout)        
        for log in logs:
            logging.info('Container_'+id+'LOG :: '+log)
    
        logging.info(get_time() +'container_'+id+': Execution complete!!')	
        
    except Exception as e:
        logging.info('Exception ')
        logging.info(e)
        logging.info(traceback.print_exc())


def stop_container(id):
    try:
        container = client.containers.get('container_'+str(id))
        if container:
            logging.info(get_time() + 'container_'+id+' stopping!!')
            container.pause()
            time.sleep(2)
            container.stop()
    except Exception as e:
        logging.info(e)


def remove_containers():
    while client.containers.list():		
        try:
            for c in client.containers.list():
                c.stop()
                c.remove()
        except Exception as e:
            print(e)


def resume_container(url, id, script_name, iteration_count, container_timeout):
    container = client.containers.get('container_'+str(id))
    if container:
        logging.info(get_time() + 'container_'+id+'_'+str(iteration_count)+' resuming!!')
        container.start()
        ## wait for display to be activated ##
        time.sleep(10)
        ##   Open a blank page on the browser and wait for notifications 
        execute_script('about:blank',id, script_name, iteration_count, container_timeout-100)


def export(container, tar_path, archive_path):
    with open(tar_path, 'w') as f:
        bits, stat = container.get_archive(archive_path)
        for chunk in bits:
            f.write(chunk)


def export_container(id, count):
    container = client.containers.get('container_' + str(id))
    logging.info(get_time() + 'container_'+id+'_'+str(count)+' exporting files!!')
    dir_path = export_path+id+'/'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    dir_path += str(count)+'/'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    export(container, dir_path+'screenshots.tar', '/home/pptruser/screenshots/')
    export(container, dir_path+'logs.tar', '/home/pptruser/logs/')
    export(container, dir_path+'resources.tar', '/home/pptruser/resources/')
    export(container, dir_path+'dowanloads.tar', '/home/pptruser/Downloads/')
    export(container, dir_path+'chrome_log.tar', '/home/pptruser/chromium/chrome_debug.log')

    # with open(dir_path+'screenshots.tar', 'wb') as f:
    #     bits, stat = container.get_archive('/home/pptruser/screenshots/')
    #     for chunk in bits:
    #         f.write(chunk)
    # with open(dir_path+'logs.tar', 'wb') as f:
    #     bits, stat = container.get_archive('/home/pptruser/logs/')
    #     for chunk in bits:
    #         f.write(chunk)
    # with open(dir_path+'resources.tar', 'wb') as f:
    #     bits, stat = container.get_archive('/home/pptruser/resources/')
    #     for chunk in bits:
    #         f.write(chunk)
    # with open(dir_path+'dowanloads.tar', 'wb') as f:
    #     bits, stat = container.get_archive('/home/pptruser/Downloads/')
    #     for chunk in bits:
    #         f.write(chunk)
    # with open(dir_path+'chrome_log.tar', 'wb') as f:
    #     bits, stat = container.get_archive('/home/pptruser/chromium/chrome_debug.log')
    #     for chunk in bits:
    #         f.write(chunk)

    return check_if_success(id,count)



def check_if_success(id,count):
    import tarfile
    logging.info(get_time() + 'container_'+id+' checking status!!')
    log_tar_dir = export_path+id+'/'+str(count)+'/logs.tar'
    t = tarfile.open(log_tar_dir,'r')
    log_name = 'logs/'+id+'_sw.log'
    res=-99
    if log_name in t.getnames():
        f = t.extractfile(log_name)
        data = f.read()
        res = data.find('Service Worker Registered')
    if res>-1:
        return True
    return False
		


def test():
    id = str(time.time()) + '_chromium'
    url = 'https://www.indiatoday.in/'
    remove_containers()
    initiate_container(url, id, 'capture_notifications.js', '0', 180)    
    count = 1
    while count < 3:
        stop_container(id)
        export_container(id, str(count-1))
        time.sleep(60)
        resume_container(url, id,'capture_notifications.js', count, 180)
        count += 1
    
    logging.info(check_if_success(id,'0'))
   
    
if __name__== "__main__":
    test()

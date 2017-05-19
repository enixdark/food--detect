import time
import PIL
from PIL import Image
from PIL import ImageEnhance
import sys, os, subprocess, shutil
from PIL import ImageFilter
import multiprocessing

def rotate_by_degree(img, rotflag):
    if rotflag == 270:
        img = img.transpose(PIL.Image.ROTATE_270)
    elif rotflag == 90:
        img = img.transpose(PIL.Image.ROTATE_90)
    elif rotflag == 180:
        img = img.transpose(PIL.Image.ROTATE_180)
    elif rotflag != 0:
        raise Exception("Unknown rotation flag({})".format(rotflag))
    return img

def blur_image(dest, sub_folder, blur_radius, brightness, file, img):
    sub_dest_path = os.path.join(dest, sub_folder)
    print(os.path.join(sub_dest_path, file))
    enhancer = ImageEnhance.Brightness(img)
    bright = enhancer.enhance(brightness)
    blurred_image = bright.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    blurred_image.save(os.path.join(sub_dest_path, "blur-" + file))

def image_processing(src, dest, sub_folder, rotate_degrees, blur_radius, brightness, files):
    i = 1;
    sub_path = os.path.join(src, sub_folder)
    for file in files:
        if file.endswith(".JPG") or file.endswith(".jpg"):
            print(os.path.join(sub_path, file))
            img = Image.open(os.path.join(sub_path, file))
            for rotation_degree in rotate_degrees:
                rotated_image = rotate_by_degree(img, int(rotation_degree))
                rotated_image.save(
                    os.path.join(os.path.join(dest, sub_folder), str(rotation_degree) + "-" + str(i) + ".jpg"))
                blur_image(dest, sub_folder, blur_radius, brightness, str(rotation_degree) + "-" + str(i) + ".jpg",
                           rotated_image)
            img.save(os.path.join(os.path.join(dest, sub_folder), str(i) + ".jpg"))
            blur_image(dest, sub_folder, blur_radius, brightness, str(i) + ".jpg", img)
            i = i + 1
            time.sleep(0.5)

def spawn_process(num_processes, src, dest, sub_folder, rotate_degrees, blur_radius, brightness, files):
    worker_jobs = []
    sub_files_for_a_job = []
    for i in range(num_processes):
        sub_files_for_a_job.append(files[i * int(len(files) / num_processes):(i + 1) * int(len(files) / num_processes)])
    for i in range(num_processes):
        p = multiprocessing.Process(target=image_processing,
                                    args=(src, dest, sub_folder, rotate_degrees, blur_radius, brightness,
                                          sub_files_for_a_job[i],))
        worker_jobs.append(p)
        p.start()

def training(src, dest, num_processes, rotate_degrees, blur_radius, brightness):
    rotate_degrees = str(rotate_degrees).split(',')
    s3_download = False
    if not os.path.exists(dest):
        os.makedirs(dest)

    for root, dirs, img in os.walk(src):
        for root, dirs, img in os.walk(src):
            for sub_folder in (dirs):
                if not os.path.exists(os.path.join(dest, sub_folder)):
                    os.makedirs(os.path.join(dest, sub_folder))
                files = os.listdir(os.path.join(src, sub_folder))
                p = multiprocessing.Process(target=spawn_process,
                                            args=(
                                                num_processes, src, dest, sub_folder, rotate_degrees, blur_radius,
                                                brightness,
                                                files,))
                p.start()
                p.join()

    if s3_download:
        shutil.rmtree(src, ignore_errors=True)

        # aws = AWS()
        # aws.upload(model_version, dest, split=True)
        # shutil.rmtree(dest, ignore_errors=True)

if __name__ == "__main__":
    src = sys.argv[1]
    dest = sys.argv[2]
    num_processes = int(sys.argv[3])
    rotate_degrees = sys.argv[4]
    blur_radius = int(sys.argv[5])
    brightness = float(sys.argv[6])
    training(src, dest, num_processes, rotate_degrees, blur_radius, brightness)

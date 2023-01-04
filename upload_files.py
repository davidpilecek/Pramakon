import subprocess 

result = subprocess.run(["./gdrive", "upload", "--recursive", "cvPics/", "-p", "1xhbGwuUqqbZ6ftwg7GMuW4ioxhQ13qsr"])

print(result.returncode)


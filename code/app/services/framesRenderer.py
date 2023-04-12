import subprocess

def run_video_drawer(input_file):
    use_billboards = "F"
    jiggly_transitions = "F"
    subprocess.run(["python3", "code/videoDrawer.py", "--input_file", input_file, "--use_billboards", use_billboards, "--jiggly_transitions", jiggly_transitions])


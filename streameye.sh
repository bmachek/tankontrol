#!/usr/bin/env bash

ffmpeg -v quiet -input_format mjpeg -video_size 640x360 -i /dev/video0 -c copy -f mjpeg - | streameye

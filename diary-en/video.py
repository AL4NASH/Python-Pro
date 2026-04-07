#!/usr/bin/env python3
"""
Video Compression Script
Reduces video file size using FFmpeg with configurable quality settings.
"""

import os
import sys
import argparse
import ffmpeg
import time
import threading
from pathlib import Path


def get_video_info(input_path):
    """Get video file information."""
    try:
        probe = ffmpeg.probe(input_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        if video_stream:
            duration = float(video_stream['duration'])
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            bitrate = int(video_stream.get('bit_rate', 0))
            fps = eval(video_stream.get('r_frame_rate', '0/1'))
            
            return {
                'duration': duration,
                'width': width,
                'height': height,
                'bitrate': bitrate,
                'fps': fps,
                'size': os.path.getsize(input_path)
            }
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None


def show_progress(duration):
    """Show progress bar during compression."""
    start_time = time.time()
    symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    i = 0
    
    while True:
        elapsed = time.time() - start_time
        if duration > 0:
            percentage = min(100, (elapsed / duration) * 100)
        else:
            percentage = min(100, elapsed * 10)  # Fallback if no duration
        
        bar_length = 40
        filled_length = int(bar_length * percentage / 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        sys.stdout.write(f'\r{symbols[i % len(symbols)]} Comprimiendo [{bar}] {percentage:.1f}%')
        sys.stdout.flush()
        
        if elapsed >= duration and duration > 0:
            break
            
        time.sleep(0.1)
        i += 1


def compress_video(input_path, output_path, quality='medium', preset='medium'):
    """
    Compress video using FFmpeg.
    
    Args:
        input_path: Path to input video
        output_path: Path to output video
        quality: Compression quality (low, medium, high)
        preset: Encoding speed preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
    """
    
    # Quality settings (CRF values for H.264)
    quality_settings = {
        'low': 28,    # Lower quality, smaller file
        'medium': 23, # Good balance
        'high': 18    # Higher quality, larger file
    }
    
    crf = quality_settings.get(quality, 23)
    
    try:
        # Get input video info
        input_info = get_video_info(input_path)
        if input_info:
            print(f"Original video info:")
            print(f"  Size: {input_info['size'] / (1024*1024):.2f} MB")
            print(f"  Duration: {input_info['duration']:.2f} seconds")
            print(f"  Resolution: {input_info['width']}x{input_info['height']}")
            print(f"  FPS: {input_info['fps']:.2f}")
            print(f"  Bitrate: {input_info['bitrate'] / 1000:.0f} kbps")
        
        print(f"\nCompressing with CRF={crf}, preset={preset}...")
        
        # Start progress indicator in separate thread
        progress_thread = threading.Thread(target=show_progress, args=(input_info['duration'] if input_info else 0,))
        progress_thread.daemon = True
        progress_thread.start()
        
        # Compress video using FFmpeg
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec='libx264',
                crf=crf,
                preset=preset,
                acodec='aac',
                audio_bitrate='128k'
            )
            .overwrite_output()
            .run(quiet=True, capture_stdout=True, capture_stderr=True)
        )
        
        # Clear progress line
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
        
        # Get output video info
        output_info = get_video_info(output_path)
        if input_info and output_info:
            compression_ratio = (1 - output_info['size'] / input_info['size']) * 100
            print(f"\nCompression complete!")
            print(f"Original size: {input_info['size'] / (1024*1024):.2f} MB")
            print(f"Compressed size: {output_info['size'] / (1024*1024):.2f} MB")
            print(f"Compression ratio: {compression_ratio:.1f}%")
            print(f"Output saved to: {output_path}")
        
        return True
        
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if hasattr(e, 'stderr') and e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"Error compressing video: {e}")
        return False


def batch_compress(input_dir, output_dir, quality='medium', preset='medium'):
    """Compress all videos in a directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Input directory does not exist: {input_dir}")
        return
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Supported video extensions
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    
    videos = [f for f in input_path.iterdir() if f.suffix.lower() in video_extensions]
    
    if not videos:
        print(f"No video files found in {input_dir}")
        return
    
    print(f"Found {len(videos)} video files")
    
    for video_file in videos:
        output_file = output_path / f"compressed_{video_file.name}"
        print(f"\nProcessing: {video_file.name}")
        compress_video(str(video_file), str(output_file), quality, preset)


def main():
    parser = argparse.ArgumentParser(description='Compress video files to reduce file size')
    parser.add_argument('input', help='Input video file or directory')
    parser.add_argument('-o', '--output', help='Output video file or directory')
    parser.add_argument('-q', '--quality', choices=['low', 'medium', 'high'], 
                       default='medium', help='Compression quality (default: medium)')
    parser.add_argument('-p', '--preset', 
                       choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 
                               'medium', 'slow', 'slower', 'veryslow'],
                       default='medium', help='Encoding speed preset (default: medium)')
    parser.add_argument('-b', '--batch', action='store_true', 
                       help='Process all videos in directory')
    
    args = parser.parse_args()
    
    if args.batch:
        # Batch processing
        output_dir = args.output or f"{args.input}_compressed"
        batch_compress(args.input, output_dir, args.quality, args.preset)
    else:
        # Single file processing
        if not args.output:
            input_path = Path(args.input)
            args.output = str(input_path.parent / f"compressed_{input_path.name}")
        
        compress_video(args.input, args.output, args.quality, args.preset)


if __name__ == "__main__":
    main()
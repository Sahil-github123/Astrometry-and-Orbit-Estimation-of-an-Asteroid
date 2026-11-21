import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# 1. Create a uniform time grid spanning the full 20 days (e.g. 1 step every 4 hours)
jd_start, jd_end = jds[0], jds[-1]
time_grid = np.linspace(jd_start, jd_end, num=120)  # 120 smooth time steps

# 2. Interpolate asteroid pixel coordinates over continuous time
interp_x = np.interp(time_grid, jds, ast_x_ref)
interp_y = np.interp(time_grid, jds, ast_y_ref)

# Map each continuous time step to the closest real observation background frame
frame_indices = [np.argmin(np.abs(jds - t)) for t in time_grid]

# 3. Animate using constant time steps
def update_smooth(step):
    bg_idx = frame_indices[step]
    img_display.set_data(reprojected_images[bg_idx])
    
    # Smooth trail and target position
    curr_marker.set_data([interp_x[step]], [interp_y[step]])
    trail_line.set_data(interp_x[:step + 1], interp_y[:step + 1])
    
    # Time elapsed display
    day_offset = time_grid[step] - jd_start
    title_text.set_text(f"Day +{day_offset:.1f} / {total_days:.1f} days")
    progress_text.set_text(f"Background: Frame {bg_idx + 1} ({files[bg_idx][:14]})")
    
    return img_display, curr_marker, trail_line, title_text, progress_text

ani = animation.FuncAnimation(fig, update_smooth, frames=len(time_grid), interval=60, blit=False)
ani.save("asteroid_time_scaled.gif", writer="pillow", fps=16, dpi=130)
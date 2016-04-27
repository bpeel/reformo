#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <inttypes.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>

#define WIDTH (1920 / 2)
#define HEIGHT (1080 / 2)

struct image {
        SDL_Texture *texture;
        char *filename;
};

struct data {
        SDL_Window *window;
        SDL_Renderer *renderer;
        struct image *images;
        int n_images;
        int current_image;
        bool quit;
        bool redraw_queued;
};

static bool
load_images(struct data *data,
            const char **filenames,
            int n_images)
{
        int i;

        data->images = malloc(sizeof data->images[0] * n_images);

        for (i = 0; i < n_images; i++) {
                data->images[i].texture =
                        IMG_LoadTexture(data->renderer, filenames[i]);
                if (data->images[i].texture == NULL) {
                        fprintf(stderr, "Failed to load %s\n", filenames[i]);
                        goto error;
                }
        }

        data->n_images = n_images;

        for (i = 0; i < n_images; i++)
                data->images[i].filename = strdup(filenames[i]);

        return true;

error:
        while (i > 0) {
                i--;
                SDL_DestroyTexture(data->images[i].texture);
        }

        free(data->images);

        return false;
}

static void
destroy_images(struct data *data)
{
        int i;

        for (i = 0; i < data->n_images; i++) {
                SDL_DestroyTexture(data->images[i].texture);
                free(data->images[i].filename);
        }

        free(data->images);
}

static void
redraw(struct data *data)
{
        SDL_SetRenderDrawColor(data->renderer, 0, 0, 0, 255);
        SDL_RenderClear(data->renderer);

        SDL_RenderCopy(data->renderer,
                       data->images[data->current_image].texture,
                       NULL, /* src_rect */
                       NULL /* dst_rect */);
        SDL_RenderPresent(data->renderer);

        data->redraw_queued = false;
}

static void
time_current_image(struct data *data)
{
        printf("%" PRIu32 " %s\n",
               SDL_GetTicks(),
               data->images[data->current_image].filename);
}

static void
set_image(struct data *data,
          int image)
{
        if (image < 0)
                image = 0;
        else if (image >= data->n_images)
                image = data->n_images - 1;

        if (image == data->current_image)
                return;

        data->current_image = image;
        data->redraw_queued = true;

        time_current_image(data);
}

static void
handle_window_event(struct data *data,
                    const struct SDL_WindowEvent *event)
{
        switch (event->event) {
        case SDL_WINDOWEVENT_SIZE_CHANGED:
        case SDL_WINDOWEVENT_EXPOSED:
                data->redraw_queued = true;
                break;
        case SDL_WINDOWEVENT_CLOSE:
                data->quit = true;
                break;
        }
}

static void
handle_key_down(struct data *data,
                const SDL_KeyboardEvent *event)
{
        switch (event->keysym.sym) {
        case SDLK_PAGEDOWN:
        case SDLK_SPACE:
                set_image(data, data->current_image + 1);
                break;
        case SDLK_PAGEUP:
                set_image(data, data->current_image - 1);
                break;
        }
}

static void
handle_event(struct data *data,
             const SDL_Event *event)
{
        switch (event->type) {
        case SDL_KEYDOWN:
                handle_key_down(data, &event->key);
                break;
        case SDL_WINDOWEVENT:
                handle_window_event(data, &event->window);
                break;
        case SDL_QUIT:
                data->quit = true;
                break;
        }
}

static void
main_loop(struct data *data)
{
        SDL_Event event;
        bool had_event;

        while (!data->quit) {
                if (data->redraw_queued)
                        had_event = SDL_PollEvent(&event);
                else
                        had_event = SDL_WaitEvent(&event);

                if (had_event)
                        handle_event(data, &event);
                else
                        redraw(data);
        }
}

int
main(int argc, const char **argv)
{
        struct data data;
        int ret = EXIT_SUCCESS;
        int res;

        memset(&data, 0, sizeof data);

        if (argc <= 1) {
                fprintf(stderr, "usage: maketiming <image>...\n");
                ret = EXIT_FAILURE;
                goto out;
        }

        res = SDL_Init(SDL_INIT_VIDEO | SDL_INIT_JOYSTICK);
        if (res < 0) {
                fprintf(stderr, "Unable to init SDL: %s\n", SDL_GetError());
                ret = EXIT_FAILURE;
                goto out;
        }

        data.window = SDL_CreateWindow("MakeTiming",
                                       SDL_WINDOWPOS_UNDEFINED,
                                       SDL_WINDOWPOS_UNDEFINED,
                                       WIDTH, HEIGHT,
                                       0 /* flags */);
        if (data.window == NULL) {
                fprintf(stderr,
                        "Failed to create SDL window: %s",
                        SDL_GetError());
                ret = EXIT_FAILURE;
                goto out_sdl;
        }

        data.renderer = SDL_CreateRenderer(data.window,
                                           -1, /* driver index */
                                           SDL_RENDERER_ACCELERATED);
        if (data.renderer == NULL) {
                fprintf(stderr,
                        "Failed to create SDL renderer: %s",
                        SDL_GetError());
                ret = EXIT_FAILURE;
                goto out_window;
        }

        if (!load_images(&data, argv + 1, argc - 1))
                goto out_renderer;

        data.current_image = -1;
        set_image(&data, 0);

        main_loop(&data);

        time_current_image(&data);

        destroy_images(&data);
out_renderer:
        SDL_DestroyRenderer(data.renderer);
out_window:
        SDL_DestroyWindow(data.window);
out_sdl:
        SDL_Quit();
out:
        return ret;
}

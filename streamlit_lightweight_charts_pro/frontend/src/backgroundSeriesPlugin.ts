/**
 * Background Series Plugin for lightweight-charts.
 * 
 * This plugin renders a background shade that changes color based on indicator values.
 * The color is interpolated between minColor and maxColor based on the data value.
 * Based on the TradingView background-shade-series plugin example.
 */

import {
    CustomSeriesOptions,
    ICustomSeriesPaneView,
    PaneRendererCustomData,
    WhitespaceData,
    Time,
    ICustomSeriesPaneRenderer,
    BitmapCoordinatesRenderingScope,
} from 'lightweight-charts';

/**
 * Background data point interface.
 */
export interface BackgroundData extends WhitespaceData {
    value: number;
    minColor: string;
    maxColor: string;
}

/**
 * Background series options interface.
 */
export interface BackgroundSeriesOptions extends CustomSeriesOptions {
    opacity?: number;
}

/**
 * Default options for background series.
 */
const defaultOptions: BackgroundSeriesOptions = {
    ...CustomSeriesOptions,
    opacity: 0.2,
};

/**
 * Interpolate between two colors based on a value.
 * 
 * @param minColor - Color for minimum value (hex format)
 * @param maxColor - Color for maximum value (hex format)
 * @param value - Value between 0 and 1
 * @returns Interpolated color in rgba format
 */
function interpolateColor(minColor: string, maxColor: string, value: number): string {
    // Convert hex to RGB
    const hexToRgb = (hex: string): [number, number, number] => {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result
            ? [
                  parseInt(result[1], 16),
                  parseInt(result[2], 16),
                  parseInt(result[3], 16),
              ]
            : [0, 0, 0];
    };

    const [r1, g1, b1] = hexToRgb(minColor);
    const [r2, g2, b2] = hexToRgb(maxColor);

    // Interpolate
    const r = Math.round(r1 + (r2 - r1) * value);
    const g = Math.round(g1 + (g2 - g1) * value);
    const b = Math.round(b1 + (b2 - b1) * value);

    return `rgb(${r}, ${g}, ${b})`;
}

/**
 * Background series renderer.
 */
class BackgroundSeriesRenderer implements ICustomSeriesPaneRenderer {
    private _data: PaneRendererCustomData<Time, BackgroundData> | null = null;
    private _options: BackgroundSeriesOptions | null = null;

    draw(
        target: BitmapCoordinatesRenderingScope,
        priceConverter: (price: number) => number
    ): void {
        if (!this._data || this._data.bars.length === 0 || !this._options) {
            return;
        }

        const ctx = target.context;
        const bars = this._data.bars;

        // Save context state
        ctx.save();

        // Set global alpha for opacity
        ctx.globalAlpha = this._options.opacity || 0.2;

        // Draw background for each bar
        for (let i = 0; i < bars.length; i++) {
            const bar = bars[i];
            const nextBar = bars[i + 1];

            if (!bar.originalData.value) {
                continue;
            }

            // Calculate color based on value
            const value = Math.max(0, Math.min(1, bar.originalData.value));
            const color = interpolateColor(
                bar.originalData.minColor,
                bar.originalData.maxColor,
                value
            );

            // Set fill color
            ctx.fillStyle = color;

            // Calculate rectangle dimensions
            const x = bar.x;
            const width = nextBar ? nextBar.x - bar.x : target.bitmapSize.width - bar.x;
            const y = 0;
            const height = target.bitmapSize.height;

            // Draw rectangle
            ctx.fillRect(x, y, width, height);
        }

        // Restore context state
        ctx.restore();
    }

    update(
        data: PaneRendererCustomData<Time, BackgroundData> | null,
        options: BackgroundSeriesOptions
    ): void {
        this._data = data;
        this._options = options;
    }
}

/**
 * Background series pane view.
 */
export class BackgroundSeriesPaneView implements ICustomSeriesPaneView {
    private _renderer: BackgroundSeriesRenderer = new BackgroundSeriesRenderer();

    renderer(): ICustomSeriesPaneRenderer {
        return this._renderer;
    }

    update(
        data: PaneRendererCustomData<Time, BackgroundData> | null,
        options: BackgroundSeriesOptions
    ): void {
        this._renderer.update(data, options);
    }

    zOrder(): 'bottom' | 'normal' | 'top' {
        return 'bottom'; // Render behind everything else
    }
}

/**
 * Background series class.
 */
export class BackgroundSeries {
    public customSeriesView(): ICustomSeriesPaneView {
        return new BackgroundSeriesPaneView();
    }

    public defaultOptions(): CustomSeriesOptions {
        return defaultOptions;
    }
}
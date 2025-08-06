import { MutableRefObject } from 'react';
import {
  IChartApi,
  ISeriesApi,
  AreaSeries,
  LineSeries,
  BarSeries,
  CandlestickSeries,
  HistogramSeries,
  BaselineSeries,
  createSeriesMarkers,
} from 'lightweight-charts';
import { SeriesConfig } from '../types';
import { BandData, createBandSeries } from '../bandSeriesPlugin';
import { SignalSeries, createSignalSeriesPlugin } from '../signalSeriesPlugin';
import { cleanLineStyleOptions } from './lineStyle';

interface SeriesFactoryContext {
  signalPluginRefs?: MutableRefObject<{ [key: string]: SignalSeries }>;
}

export function createSeries(
  chart: IChartApi,
  seriesConfig: SeriesConfig,
  context: SeriesFactoryContext = {},
  chartId?: string,
  seriesIndex?: number,
): ISeriesApi<any> | null {
  const { signalPluginRefs } = context;

  const {
    type,
    data,
    options = {},
    priceScale,
    paneId,
    lastValueVisible: topLevelLastValueVisible,
    lastPriceAnimation,
    priceLineVisible: topLevelPriceLineVisible,
    priceLineSource: topLevelPriceLineSource,
    priceLineWidth: topLevelPriceLineWidth,
    priceLineColor: topLevelPriceLineColor,
    priceLineStyle: topLevelPriceLineStyle,
    priceScaleId: topLevelPriceScaleId,
  } = seriesConfig;

  const lastValueVisible =
    topLevelLastValueVisible !== undefined ? topLevelLastValueVisible : options.lastValueVisible;
  const priceLineVisible =
    topLevelPriceLineVisible !== undefined ? topLevelPriceLineVisible : options.priceLineVisible;
  const priceLineSource =
    topLevelPriceLineSource !== undefined ? topLevelPriceLineSource : options.priceLineSource;
  const priceLineWidth =
    topLevelPriceLineWidth !== undefined ? topLevelPriceLineWidth : options.priceLineWidth;
  const priceLineColor =
    topLevelPriceLineColor !== undefined ? topLevelPriceLineColor : options.priceLineColor;
  const priceLineStyle =
    topLevelPriceLineStyle !== undefined ? topLevelPriceLineStyle : options.priceLineStyle;
  const priceScaleId =
    topLevelPriceScaleId !== undefined ? topLevelPriceScaleId : options.priceScaleId;

  let series: ISeriesApi<any>;
  const normalizedType = type?.toLowerCase();
  const { priceFormat, ...otherOptions } = options;
  const cleanedOptions = cleanLineStyleOptions(otherOptions);

  switch (normalizedType) {
    case 'area': {
      const areaOptions: any = {
        ...cleanedOptions,
        lineColor: cleanedOptions.lineColor || '#2196F3',
        topColor: cleanedOptions.topColor || 'rgba(33, 150, 243, 0.4)',
        bottomColor: cleanedOptions.bottomColor || 'rgba(33, 150, 243, 0.0)',
        lineWidth: cleanedOptions.lineWidth || 2,
        relativeGradient: cleanedOptions.relativeGradient || false,
        invertFilledArea: cleanedOptions.invertFilledArea || false,
        priceScaleId: priceScaleId || '',
        lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
        lastPriceAnimation: lastPriceAnimation !== undefined ? lastPriceAnimation : 0,
        priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
        priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
        priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
        priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
        priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2,
      };
      if (priceFormat) {
        areaOptions.priceFormat = priceFormat;
      }
      series = chart.addSeries(AreaSeries, areaOptions, paneId);
      try {
        if (lastValueVisible === false) {
          series.applyOptions({ lastValueVisible: false });
        }
      } catch {
        // ignore
      }
      break;
    }
    case 'band': {
      try {
        const bandSeriesOptions: any = {
          upperLine: cleanedOptions.upperLine || {
            color: '#4CAF50',
            lineStyle: 0,
            lineWidth: 2,
            lineVisible: true,
          },
          middleLine: cleanedOptions.middleLine || {
            color: '#2196F3',
            lineStyle: 0,
            lineWidth: 2,
            lineVisible: true,
          },
          lowerLine: cleanedOptions.lowerLine || {
            color: '#F44336',
            lineStyle: 0,
            lineWidth: 2,
            lineVisible: true,
          },
          upperFillColor: cleanedOptions.upperFillColor || 'rgba(76, 175, 80, 0.1)',
          lowerFillColor: cleanedOptions.lowerFillColor || 'rgba(244, 67, 54, 0.1)',
          priceScaleId: priceScaleId || 'right',
          visible: cleanedOptions.visible !== false,
          lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
          priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
          priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
          priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
          priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
          priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2,
        };
        const bandSeries = createBandSeries(chart, bandSeriesOptions);
        if (data && data.length > 0) {
          bandSeries.setData(data as BandData[]);
        }
        return {
          setData: (newData: any[]) => {
            try {
              bandSeries.setData(newData as BandData[]);
            } catch {}
          },
          update: (newData: any) => {
            try {
              bandSeries.update(newData as BandData);
            } catch {}
          },
          applyOptions: (options: any) => {
            try {
              bandSeries.setOptions(cleanLineStyleOptions(options));
            } catch {}
          },
          priceScale: () => {
            try {
              return chart.priceScale(priceScaleId || 'right');
            } catch {
              return null;
            }
          },
          remove: () => {
            try {
              bandSeries.remove();
            } catch {}
          },
        } as unknown as ISeriesApi<any>;
      } catch {
        return null;
      }
    }
    case 'signal': {
      try {
        const signalSeries = createSignalSeriesPlugin(chart, {
          type: 'signal',
          data: data || [],
          options: {
            neutralColor: cleanedOptions.neutralColor || '#f0f0f0',
            signalColor: cleanedOptions.signalColor || '#ff0000',
            alertColor: cleanedOptions.alertColor,
            visible: cleanedOptions.visible !== false,
          },
          paneId: paneId,
        });
        if (signalPluginRefs && chartId !== undefined && seriesIndex !== undefined) {
          signalPluginRefs.current[`${chartId}-${seriesIndex}`] = signalSeries;
        }
        return {
          setData: (newData: any[]) => {
            try {
              signalSeries.updateData(newData);
            } catch {}
          },
          update: (newData: any) => {
            try {
              signalSeries.updateData([newData]);
            } catch {}
          },
          applyOptions: (options: any) => {
            try {
              signalSeries.updateOptions({
                neutralColor: options.neutralColor || '#f0f0f0',
                signalColor: options.signalColor || '#ff0000',
                alertColor: options.alertColor,
                visible: options.visible !== false,
              });
            } catch {}
          },
          priceScale: () => {
            try {
              return chart.priceScale(priceScaleId || 'right');
            } catch {
              return null;
            }
          },
          remove: () => {
            try {
              signalSeries.destroy();
              if (signalPluginRefs && chartId !== undefined && seriesIndex !== undefined) {
                delete signalPluginRefs.current[`${chartId}-${seriesIndex}`];
              }
            } catch {}
          },
        } as unknown as ISeriesApi<any>;
      } catch {
        return null;
      }
    }
    case 'baseline': {
      const baselineOptions: any = {
        ...cleanedOptions,
        baseValue: cleanedOptions.baseValue || { price: 0 },
        topLineColor: cleanedOptions.topLineColor || 'rgba(76, 175, 80, 0.4)',
        topFillColor1: cleanedOptions.topFillColor1 || 'rgba(76, 175, 80, 0.0)',
        topFillColor2: cleanedOptions.topFillColor2 || 'rgba(76, 175, 80, 0.4)',
        bottomLineColor: cleanedOptions.bottomLineColor || 'rgba(255, 82, 82, 0.4)',
        bottomFillColor1: cleanedOptions.bottomFillColor1 || 'rgba(255, 82, 82, 0.4)',
        bottomFillColor2: cleanedOptions.bottomFillColor2 || 'rgba(255, 82, 82, 0.0)',
        lineWidth: cleanedOptions.lineWidth || 2,
        priceScaleId: priceScaleId || '',
        lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
        priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
        priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
        priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
        priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
        priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2,
      };
      if (priceFormat) {
        baselineOptions.priceFormat = priceFormat;
      }
      series = chart.addSeries(BaselineSeries, baselineOptions, paneId);
      break;
    }
    case 'histogram': {
      const histogramOptions: any = {
        ...cleanedOptions,
        priceFormat: priceFormat || {
          type: 'volume',
        },
        priceScaleId: priceScaleId || '',
        scaleMargins: cleanedOptions.scaleMargins || {
          top: 0.75,
          bottom: 0,
        },
        lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
        color: cleanedOptions.color || '#2196F3',
        priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
        priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
        priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
        priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
        priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2,
      };
      if (priceFormat) {
        histogramOptions.priceFormat = priceFormat;
      }
      series = chart.addSeries(HistogramSeries, histogramOptions, paneId);
      break;
    }
    case 'line': {
      const lineOptions: any = {
        ...cleanedOptions,
        color: cleanedOptions.color || '#FF9800',
        lineWidth: cleanedOptions.lineWidth || 2,
        crossHairMarkerVisible: cleanedOptions.crossHairMarkerVisible || true,
        priceScaleId: priceScaleId || '',
        lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
        priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
        priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
        priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
        priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
        priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2,
      };
      if (priceFormat) {
        lineOptions.priceFormat = priceFormat;
      }
      series = chart.addSeries(LineSeries, lineOptions, paneId);
      break;
    }
    case 'bar': {
      const barOptions: any = {
        ...cleanedOptions,
        upColor: cleanedOptions.upColor || '#4CAF50',
        downColor: cleanedOptions.downColor || '#F44336',
        openVisible: cleanedOptions.openVisible || false,
        priceScaleId: priceScaleId || '',
        lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
        priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
        priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
        priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
        priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
        priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2,
      };
      if (priceFormat) {
        barOptions.priceFormat = priceFormat;
      }
      series = chart.addSeries(BarSeries, barOptions, paneId);
      break;
    }
    case 'candlestick': {
      const candlestickOptions: any = {
        ...cleanedOptions,
        upColor: cleanedOptions.upColor || '#4CAF50',
        downColor: cleanedOptions.downColor || '#F44336',
        borderVisible: cleanedOptions.borderVisible !== false,
        wickUpColor: cleanedOptions.wickUpColor || '#4CAF50',
        wickDownColor: cleanedOptions.wickDownColor || '#F44336',
        priceScaleId: priceScaleId || '',
        lastValueVisible: lastValueVisible !== undefined ? lastValueVisible : true,
        priceLineVisible: priceLineVisible !== undefined ? priceLineVisible : true,
        priceLineSource: priceLineSource !== undefined ? priceLineSource : 'lastBar',
        priceLineWidth: priceLineWidth !== undefined ? priceLineWidth : 1,
        priceLineColor: priceLineColor !== undefined ? priceLineColor : '',
        priceLineStyle: priceLineStyle !== undefined ? priceLineStyle : 2,
      };
      if (priceFormat) {
        candlestickOptions.priceFormat = priceFormat;
      }
      series = chart.addSeries(CandlestickSeries, candlestickOptions, paneId);
      break;
    }
    default:
      return null;
  }

  if (priceScale) {
    series.priceScale().applyOptions(cleanLineStyleOptions(priceScale));
  }

  if (data && data.length > 0) {
    series.setData(data);
  }

  if (seriesConfig.priceLines && Array.isArray(seriesConfig.priceLines)) {
    seriesConfig.priceLines.forEach((priceLine: any, index: number) => {
      try {
        series.createPriceLine(priceLine);
      } catch (error) {
        console.warn(`❌ Failed to create price line ${index + 1} for series:`, error);
      }
    });
  }

  if (seriesConfig.markers && Array.isArray(seriesConfig.markers)) {
    try {
      createSeriesMarkers(series, seriesConfig.markers);
    } catch (error) {
      console.warn('❌ Failed to create markers for series:', error);
    }
  }

  return series;
}


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
import { createBandSeries, BandData } from '../bandSeriesPlugin';
import { SignalSeries, createSignalSeriesPlugin } from '../signalSeriesPlugin';
import { cleanLineStyleOptions } from './lineStyle';
import { createTradeVisualElements } from '../tradeVisualization';

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

  // Ensure paneId has a default value
  const finalPaneId = paneId !== undefined ? paneId : 0;

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
      series = chart.addSeries(AreaSeries, areaOptions, finalPaneId);
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
          upperFill: cleanedOptions.upperFill !== undefined ? cleanedOptions.upperFill : true,
          lowerFill: cleanedOptions.lowerFill !== undefined ? cleanedOptions.lowerFill : true,
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
          paneId: finalPaneId,
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
      series = chart.addSeries(BaselineSeries, baselineOptions, finalPaneId);
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
      series = chart.addSeries(HistogramSeries, histogramOptions, finalPaneId);
      break;
    }
    case 'line': {
      // Process lineOptions if provided
      const lineSpecificOptions = seriesConfig.lineOptions || {};
      
      const lineOptions: any = {
        ...cleanedOptions,
        // Apply line-specific options from lineOptions object
        lineStyle: lineSpecificOptions.lineStyle !== undefined ? lineSpecificOptions.lineStyle : cleanedOptions.lineStyle,
        lineType: lineSpecificOptions.lineType !== undefined ? lineSpecificOptions.lineType : cleanedOptions.lineType,
        lineVisible: lineSpecificOptions.lineVisible !== undefined ? lineSpecificOptions.lineVisible : cleanedOptions.lineVisible,
        pointMarkersVisible: lineSpecificOptions.pointMarkersVisible !== undefined ? lineSpecificOptions.pointMarkersVisible : cleanedOptions.pointMarkersVisible,
        pointMarkersRadius: lineSpecificOptions.pointMarkersRadius !== undefined ? lineSpecificOptions.pointMarkersRadius : cleanedOptions.pointMarkersRadius,
        crosshairMarkerVisible: lineSpecificOptions.crosshairMarkerVisible !== undefined ? lineSpecificOptions.crosshairMarkerVisible : cleanedOptions.crosshairMarkerVisible,
        crosshairMarkerRadius: lineSpecificOptions.crosshairMarkerRadius !== undefined ? lineSpecificOptions.crosshairMarkerRadius : cleanedOptions.crosshairMarkerRadius,
        crosshairMarkerBorderColor: lineSpecificOptions.crosshairMarkerBorderColor !== undefined ? lineSpecificOptions.crosshairMarkerBorderColor : cleanedOptions.crosshairMarkerBorderColor,
        crosshairMarkerBackgroundColor: lineSpecificOptions.crosshairMarkerBackgroundColor !== undefined ? lineSpecificOptions.crosshairMarkerBackgroundColor : cleanedOptions.crosshairMarkerBackgroundColor,
        crosshairMarkerBorderWidth: lineSpecificOptions.crosshairMarkerBorderWidth !== undefined ? lineSpecificOptions.crosshairMarkerBorderWidth : cleanedOptions.crosshairMarkerBorderWidth,
        lastPriceAnimation: lineSpecificOptions.lastPriceAnimation !== undefined ? lineSpecificOptions.lastPriceAnimation : lastPriceAnimation,
        // Default values
        color: cleanedOptions.color || '#2196F3', // Restore original default color
        lineWidth: cleanedOptions.lineWidth || 2,
        crossHairMarkerVisible: lineSpecificOptions.crosshairMarkerVisible !== undefined ? lineSpecificOptions.crosshairMarkerVisible : (cleanedOptions.crossHairMarkerVisible !== undefined ? cleanedOptions.crossHairMarkerVisible : true),
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
      series = chart.addSeries(LineSeries, lineOptions, finalPaneId);
      
      // Apply lastValueVisible: false after series creation if needed
      try {
        if (lastValueVisible === false) {
          series.applyOptions({ lastValueVisible: false });
        }
      } catch {
        // ignore
      }
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
      series = chart.addSeries(BarSeries, barOptions, finalPaneId);
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
      series = chart.addSeries(CandlestickSeries, candlestickOptions, finalPaneId);
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
      console.log('🔍 [seriesFactory] Processing series markers:', {
        markersCount: seriesConfig.markers.length,
        seriesType: seriesConfig.type,
        hasChartData: !!data,
        chartDataCount: data?.length || 0
      });
      
      // Apply timestamp snapping to all markers (like trade visualization)
      const snappedMarkers = applyTimestampSnapping(seriesConfig.markers, data);
      console.log('✅ [seriesFactory] Markers processed, calling createSeriesMarkers');
      createSeriesMarkers(series, snappedMarkers);
    } catch (error) {
      console.warn('❌ Failed to create markers for series:', error);
    }
  }

  // Store paneId as a property on the series object for legend functionality
  if (finalPaneId !== undefined) {
    (series as any).paneId = finalPaneId;
  }

  // Add trade visualization if configured for this series
      if (seriesConfig.trades && seriesConfig.tradeVisualizationOptions && seriesConfig.trades.length > 0) {
        try {
          // Create trade visual elements (markers, rectangles, annotations)
          const tradeOptions = seriesConfig.tradeVisualizationOptions;
          const visualElements = createTradeVisualElements(seriesConfig.trades, tradeOptions, data);
          
          // Add trade markers to the series
          if (visualElements.markers && visualElements.markers.length > 0) {
            createSeriesMarkers(series, visualElements.markers);
          }
          
          // Store rectangle data for later processing by the chart component
          if (visualElements.rectangles && visualElements.rectangles.length > 0) {
            // Store the rectangle data in the chart for later processing
            if (!(chart as any)._pendingTradeRectangles) {
              (chart as any)._pendingTradeRectangles = [];
            }
            (chart as any)._pendingTradeRectangles.push({
              rectangles: visualElements.rectangles,
              series: series,
              chartId: chartId
            });
          }
          
        } catch (error) {
          console.warn('❌ Failed to create trade visualization for series:', error);
        }
      }

  return series;
}

/**
 * Apply timestamp snapping to markers to ensure they align with chart data.
 * This function implements the same logic as the trade visualization system
 * but applies it to all markers, not just trade markers.
 * 
 * @param markers Array of markers to snap
 * @param chartData Chart data for timestamp reference
 * @returns Array of markers with snapped timestamps
 */
function applyTimestampSnapping(markers: any[], chartData?: any[]): any[] {
  console.log('🔍 [applyTimestampSnapping] Starting timestamp snapping for markers:', {
    markersCount: markers?.length || 0,
    chartDataCount: chartData?.length || 0,
    hasChartData: !!chartData
  });

  if (!chartData || chartData.length === 0) {
    console.log('⚠️ [applyTimestampSnapping] No chart data available, returning markers as-is');
    return markers;
  }

  // Extract available timestamps from chart data
  const availableTimes = chartData.map(item => {
    if (typeof item.time === 'number') {
      return item.time;
    } else if (typeof item.time === 'string') {
      return Math.floor(new Date(item.time).getTime() / 1000);
    }
    return null;
  }).filter(time => time !== null);

  console.log('🔍 [applyTimestampSnapping] Available chart timestamps:', {
    total: availableTimes.length,
    sample: availableTimes.slice(0, 5),
    range: availableTimes.length > 0 ? `${availableTimes[0]} to ${availableTimes[availableTimes.length - 1]}` : 'none'
  });

  if (availableTimes.length === 0) {
    console.log('⚠️ [applyTimestampSnapping] No valid timestamps available, returning markers as-is');
    return markers;
  }

  // Apply timestamp snapping to each marker
  const snappedMarkers = markers.map((marker, index) => {
    if (marker.time && typeof marker.time === 'number') {
      const originalTime = marker.time;
      
      // Find nearest available timestamp
      const nearestTime = availableTimes.reduce((nearest, current) => {
        const currentDiff = Math.abs(current - marker.time);
        const nearestDiff = Math.abs(nearest - marker.time);
        return currentDiff < nearestDiff ? current : nearest;
      });

      const timeDiff = Math.abs(originalTime - nearestTime);
      
      console.log(`🎯 [applyTimestampSnapping] Marker ${index + 1} timestamp snapping:`, {
        originalTime,
        nearestTime,
        timeDiff,
        marker: {
          text: marker.text,
          position: marker.position,
          shape: marker.shape
        }
      });

      // Return marker with snapped timestamp
      return {
        ...marker,
        time: nearestTime
      };
    } else {
      console.log(`⚠️ [applyTimestampSnapping] Marker ${index + 1} has no valid time:`, marker);
      return marker;
    }
  });

  console.log('✅ [applyTimestampSnapping] Timestamp snapping completed:', {
    inputMarkers: markers.length,
    outputMarkers: snappedMarkers.length,
    markersWithSnapping: snappedMarkers.filter(m => m.time !== markers.find(om => om.text === m.text)?.time).length
  });

  return snappedMarkers;
}


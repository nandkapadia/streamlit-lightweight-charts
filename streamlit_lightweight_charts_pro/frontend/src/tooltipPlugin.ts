/**
 * Tooltip Plugin for Lightweight Charts
 *
 * This plugin provides comprehensive tooltip functionality with support for:
 * - Dynamic content using placeholders
 * - Multiple tooltip types (OHLC, single, multi, custom, trade, marker)
 * - Flexible positioning and styling
 * - Real-time data substitution
 */

import {IChartApi, ISeriesApi, SeriesType, Time} from 'lightweight-charts'

export interface TooltipField {
  label: string
  valueKey: string
  color?: string
  fontSize?: number
  fontWeight?: string
  prefix?: string
  suffix?: string
  precision?: number
}

export interface TooltipStyle {
  backgroundColor?: string
  borderColor?: string
  borderWidth?: number
  borderRadius?: number
  padding?: number
  fontSize?: number
  fontFamily?: string
  color?: string
  boxShadow?: string
  zIndex?: number
}

export interface TooltipConfig {
  enabled: boolean
  type: 'ohlc' | 'single' | 'multi' | 'custom' | 'trade' | 'marker'
  template?: string
  fields: TooltipField[]
  position?: 'cursor' | 'fixed' | 'auto'
  offset?: {x: number; y: number}
  style?: TooltipStyle
  showDate?: boolean
  dateFormat?: string
  showTime?: boolean
  timeFormat?: string
}

export interface TooltipData {
  time: Time
  series: ISeriesApi<SeriesType>
  data: any
  price: number
  index: number
}

export class TooltipPlugin {
  private chart: IChartApi
  private container: HTMLElement
  private tooltipElement: HTMLElement | null = null
  private configs: Map<string, TooltipConfig> = new Map()
  private currentData: TooltipData | null = null
  private isVisible = false

  constructor(chart: IChartApi, container: HTMLElement) {
    this.chart = chart
    this.container = container
    this.setupEventListeners()
  }

  /**
   * Add tooltip configuration
   */
  addConfig(name: string, config: TooltipConfig): void {
    this.configs.set(name, config)
  }

  /**
   * Remove tooltip configuration
   */
  removeConfig(name: string): boolean {
    return this.configs.delete(name)
  }

  /**
   * Get tooltip configuration
   */
  getConfig(name: string): TooltipConfig | undefined {
    return this.configs.get(name)
  }

  /**
   * Setup event listeners for tooltip functionality
   */
  private setupEventListeners(): void {
    // Subscribe to crosshair move events
    this.chart.subscribeCrosshairMove(param => {
      if (param.time && param.seriesData.size > 0) {
        this.showTooltip(param)
      } else {
        this.hideTooltip()
      }
    })

    // Subscribe to chart click events to hide tooltip
    this.chart.subscribeClick(() => {
      this.hideTooltip()
    })
  }

  /**
   * Show tooltip with data
   */
  private showTooltip(param: any): void {
    if (!this.isVisible || !param.time || param.seriesData.size === 0) {
      return
    }

    // Get the first series data
    const [series, data] = param.seriesData.entries().next().value
    if (!series || !data) {
      return
    }

    // Create tooltip data
    const tooltipData: TooltipData = {
      time: param.time,
      series,
      data,
      price: param.price || data.value || data.close || 0,
      index: param.index || 0
    }

    this.currentData = tooltipData
    this.updateTooltipContent()
    this.positionTooltip(param.point)
  }

  /**
   * Hide tooltip
   */
  private hideTooltip(): void {
    if (this.tooltipElement) {
      this.tooltipElement.style.display = 'none'
    }
    this.currentData = null
  }

  /**
   * Create tooltip element if it doesn't exist
   */
  private ensureTooltipElement(): HTMLElement {
    if (!this.tooltipElement) {
      this.tooltipElement = document.createElement('div')
      this.tooltipElement.className = 'chart-tooltip'
      this.tooltipElement.style.cssText = `
        position: absolute;
        z-index: 1000;
        background-color: rgba(255, 255, 255, 0.95);
        border: 1px solid #e1e3e6;
        border-radius: 4px;
        padding: 8px;
        font-family: sans-serif;
        font-size: 12px;
        color: #131722;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        pointer-events: none;
        user-select: none;
        white-space: nowrap;
        display: none;
      `
      this.container.appendChild(this.tooltipElement)
    }
    return this.tooltipElement
  }

  /**
   * Update tooltip content based on current data
   */
  private updateTooltipContent(): void {
    if (!this.currentData) {
      return
    }

    const tooltipElement = this.ensureTooltipElement()
    const config = this.getDefaultConfig()

    if (!config || !config.enabled) {
      return
    }

    const content = this.formatTooltipContent(config, this.currentData)
    tooltipElement.innerHTML = content

    // Apply custom styling
    if (config.style) {
      this.applyTooltipStyle(tooltipElement, config.style)
    }
  }

  /**
   * Format tooltip content using configuration
   */
  private formatTooltipContent(config: TooltipConfig, data: TooltipData): string {
    if (config.template) {
      return this.formatWithTemplate(config, data)
    } else {
      return this.formatWithFields(config, data)
    }
  }

  /**
   * Format tooltip using template with placeholders
   */
  private formatWithTemplate(config: TooltipConfig, data: TooltipData): string {
    if (!config.template) {
      return ''
    }

    let result = config.template

    // Replace placeholders with actual values
    const dataObj = this.extractDataObject(data)
    for (const [key, value] of Object.entries(dataObj)) {
      const placeholder = `{${key}}`
      if (result.includes(placeholder)) {
        const formattedValue = this.formatValue(key, value, config)
        result = result.replace(new RegExp(placeholder, 'g'), formattedValue)
      }
    }

    // Add date/time if configured
    if ((config.showDate || config.showTime) && data.time) {
      const timeStr = this.formatTime(data.time, config)
      if (timeStr) {
        result = `${timeStr}<br>${result}`
      }
    }

    return result
  }

  /**
   * Format tooltip using field configuration
   */
  private formatWithFields(config: TooltipConfig, data: TooltipData): string {
    const lines: string[] = []

    // Add date/time if configured
    if ((config.showDate || config.showTime) && data.time) {
      const timeStr = this.formatTime(data.time, config)
      if (timeStr) {
        lines.push(timeStr)
      }
    }

    // Add field values
    const dataObj = this.extractDataObject(data)
    for (const field of config.fields) {
      if (dataObj[field.valueKey] !== undefined) {
        const value = dataObj[field.valueKey]
        const formattedValue = this.formatFieldValue(field, value)
        lines.push(`${field.label}: ${formattedValue}`)
      }
    }

    return lines.join('<br>')
  }

  /**
   * Extract data object from tooltip data
   */
  private extractDataObject(data: TooltipData): any {
    const result: any = {
      time: data.time,
      price: data.price,
      value: data.data.value,
      open: data.data.open,
      high: data.data.high,
      low: data.data.low,
      close: data.data.close,
      volume: data.data.volume,
      index: data.index
    }

    // Add all properties from the data object
    Object.assign(result, data.data)

    return result
  }

  /**
   * Format a single value
   */
  private formatValue(key: string, value: any, config: TooltipConfig): string {
    const field = config.fields.find(f => f.valueKey === key)
    if (field) {
      return this.formatFieldValue(field, value)
    }
    return String(value)
  }

  /**
   * Format field value according to field configuration
   */
  private formatFieldValue(field: TooltipField, value: any): string {
    let result = String(value)

    // Apply precision for numeric values
    if (field.precision !== undefined && typeof value === 'number') {
      result = value.toFixed(field.precision)
    }

    // Add prefix and suffix
    if (field.prefix) {
      result = `${field.prefix}${result}`
    }
    if (field.suffix) {
      result = `${result}${field.suffix}`
    }

    return result
  }

  /**
   * Format time value according to configuration
   */
  private formatTime(time: Time, config: TooltipConfig): string {
    try {
      const date = new Date((time as number) * 1000)
      const parts: string[] = []

      if (config.showDate) {
        const dateFormat = config.dateFormat || '%Y-%m-%d'
        parts.push(this.formatDate(date, dateFormat))
      }

      if (config.showTime) {
        const timeFormat = config.timeFormat || '%H:%M:%S'
        parts.push(this.formatTimeString(date, timeFormat))
      }

      return parts.join(' ')
    } catch (error) {
      return String(time)
    }
  }

  /**
   * Format date according to format string
   */
  private formatDate(date: Date, format: string): string {
    // Simple date formatting - can be enhanced with a proper date library
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')

    return format.replace('%Y', String(year)).replace('%m', month).replace('%d', day)
  }

  /**
   * Format time according to format string
   */
  private formatTimeString(date: Date, format: string): string {
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')

    return format.replace('%H', hours).replace('%M', minutes).replace('%S', seconds)
  }

  /**
   * Position tooltip on the chart
   */
  private positionTooltip(point: {x: number; y: number}): void {
    if (!this.tooltipElement || !point) {
      return
    }

    const config = this.getDefaultConfig()
    if (!config) {
      return
    }

    const containerRect = this.container.getBoundingClientRect()
    const tooltipRect = this.tooltipElement.getBoundingClientRect()

    let x = point.x
    let y = point.y

    // Apply offset if configured
    if (config.offset) {
      x += config.offset.x || 0
      y += config.offset.y || 0
    }

    // Ensure tooltip stays within container bounds
    if (x + tooltipRect.width > containerRect.width) {
      x = point.x - tooltipRect.width - 10
    }

    if (y + tooltipRect.height > containerRect.height) {
      y = point.y - tooltipRect.height - 10
    }

    this.tooltipElement.style.left = `${x}px`
    this.tooltipElement.style.top = `${y}px`
    this.tooltipElement.style.display = 'block'
  }

  /**
   * Apply custom styling to tooltip element
   */
  private applyTooltipStyle(element: HTMLElement, style: TooltipStyle): void {
    if (style.backgroundColor) {
      element.style.backgroundColor = style.backgroundColor
    }
    if (style.borderColor) {
      element.style.borderColor = style.borderColor
    }
    if (style.borderWidth !== undefined) {
      element.style.borderWidth = `${style.borderWidth}px`
    }
    if (style.borderRadius !== undefined) {
      element.style.borderRadius = `${style.borderRadius}px`
    }
    if (style.padding !== undefined) {
      element.style.padding = `${style.padding}px`
    }
    if (style.fontSize !== undefined) {
      element.style.fontSize = `${style.fontSize}px`
    }
    if (style.fontFamily) {
      element.style.fontFamily = style.fontFamily
    }
    if (style.color) {
      element.style.color = style.color
    }
    if (style.boxShadow) {
      element.style.boxShadow = style.boxShadow
    }
    if (style.zIndex !== undefined) {
      element.style.zIndex = String(style.zIndex)
    }
  }

  /**
   * Get default tooltip configuration
   */
  private getDefaultConfig(): TooltipConfig | undefined {
    return this.configs.get('default') || this.configs.values().next().value
  }

  /**
   * Enable tooltip
   */
  enable(): void {
    this.isVisible = true
  }

  /**
   * Disable tooltip
   */
  disable(): void {
    this.isVisible = false
    this.hideTooltip()
  }

  /**
   * Destroy tooltip plugin
   */
  destroy(): void {
    if (this.tooltipElement) {
      this.container.removeChild(this.tooltipElement)
      this.tooltipElement = null
    }
    this.configs.clear()
    this.currentData = null
  }
}

/**
 * Create and configure tooltip plugin
 */
export function createTooltipPlugin(
  chart: IChartApi,
  container: HTMLElement,
  configs: Record<string, TooltipConfig> = {}
): TooltipPlugin {
  const plugin = new TooltipPlugin(chart, container)

  // Add configurations
  for (const [name, config] of Object.entries(configs)) {
    plugin.addConfig(name, config)
  }

  return plugin
}

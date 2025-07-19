import { Annotation, AnnotationLayer } from './types'
import { UTCTimestamp } from 'lightweight-charts'

export interface AnnotationVisualElements {
  markers: any[]
  shapes: any[]
  texts: any[]
}

export function createAnnotationVisualElements(
  annotations: Annotation[],
  layers?: AnnotationLayer[]
): AnnotationVisualElements {
  const result: AnnotationVisualElements = {
    markers: [],
    shapes: [],
    texts: []
  }

  // Process direct annotations
  for (const annotation of annotations) {
    const elements = createSingleAnnotation(annotation)
    result.markers.push(...elements.markers)
    result.shapes.push(...elements.shapes)
    result.texts.push(...elements.texts)
  }

  // Process layer annotations
  if (layers) {
    for (const layer of layers) {
      if (layer.visible) {
        for (const annotation of layer.annotations) {
          const elements = createSingleAnnotation(annotation, layer.opacity)
          result.markers.push(...elements.markers)
          result.shapes.push(...elements.shapes)
          result.texts.push(...elements.texts)
        }
      }
    }
  }

  return result
}

function createSingleAnnotation(annotation: Annotation, layerOpacity?: number): AnnotationVisualElements {
  const result: AnnotationVisualElements = {
    markers: [],
    shapes: [],
    texts: []
  }

  const opacity = layerOpacity !== undefined ? layerOpacity * (annotation.opacity || 1) : (annotation.opacity || 1)

  switch (annotation.type) {
    case 'text':
      result.texts.push(createTextAnnotation(annotation, opacity))
      break
    case 'arrow':
      result.shapes.push(createArrowAnnotation(annotation, opacity))
      break
    case 'shape':
      result.shapes.push(createShapeAnnotation(annotation, opacity))
      break
    case 'line':
      result.shapes.push(createLineAnnotation(annotation, opacity))
      break
    case 'rectangle':
      result.shapes.push(createRectangleAnnotation(annotation, opacity))
      break
    case 'circle':
      result.shapes.push(createCircleAnnotation(annotation, opacity))
      break
  }

  return result
}

function createTextAnnotation(annotation: Annotation, opacity: number): any {
  const time = parseTime(annotation.time)
  
  return {
    type: 'text',
    time: time,
    price: annotation.price,
    text: annotation.text,
    fontSize: annotation.fontSize || 12,
    fontWeight: annotation.fontWeight || 'normal',
    color: annotation.textColor || '#000000',
    backgroundColor: annotation.backgroundColor || 'rgba(255, 255, 255, 0.9)',
    borderColor: annotation.borderColor || '#CCCCCC',
    borderWidth: annotation.borderWidth || 1,
    opacity: opacity,
    padding: 4,
    tooltip: annotation.tooltip
  }
}

function createArrowAnnotation(annotation: Annotation, opacity: number): any {
  const time = parseTime(annotation.time)
  
  return {
    type: 'arrow',
    time: time,
    price: annotation.price,
    color: annotation.color || '#2196F3',
    size: annotation.fontSize || 12,
    opacity: opacity,
    text: annotation.text,
    tooltip: annotation.tooltip
  }
}

function createShapeAnnotation(annotation: Annotation, opacity: number): any {
  const time = parseTime(annotation.time)
  
  return {
    type: 'shape',
    time: time,
    price: annotation.price,
    color: annotation.color || '#2196F3',
    backgroundColor: annotation.backgroundColor || 'rgba(33, 150, 243, 0.2)',
    borderColor: annotation.borderColor || '#2196F3',
    borderWidth: annotation.borderWidth || 1,
    opacity: opacity,
    text: annotation.text,
    tooltip: annotation.tooltip
  }
}

function createLineAnnotation(annotation: Annotation, opacity: number): any {
  const time = parseTime(annotation.time)
  
  return {
    type: 'trendLine',
    time1: time,
    price1: annotation.price,
    time2: time + 86400, // 1 day later
    price2: annotation.price,
    lineColor: annotation.color || '#2196F3',
    lineWidth: annotation.borderWidth || 2,
    lineStyle: getLineStyleValue(annotation.lineStyle || 'solid'),
    opacity: opacity,
    text: annotation.text,
    tooltip: annotation.tooltip
  }
}

function createRectangleAnnotation(annotation: Annotation, opacity: number): any {
  const time = parseTime(annotation.time)
  
  return {
    type: 'rectangle',
    time1: time,
    price1: annotation.price * 0.99,
    time2: time + 86400, // 1 day later
    price2: annotation.price * 1.01,
    fillColor: annotation.backgroundColor || 'rgba(33, 150, 243, 0.2)',
    borderColor: annotation.borderColor || '#2196F3',
    borderWidth: annotation.borderWidth || 1,
    opacity: opacity,
    text: annotation.text,
    tooltip: annotation.tooltip
  }
}

function createCircleAnnotation(annotation: Annotation, opacity: number): any {
  const time = parseTime(annotation.time)
  
  return {
    type: 'circle',
    time: time,
    price: annotation.price,
    color: annotation.color || '#2196F3',
    backgroundColor: annotation.backgroundColor || 'rgba(33, 150, 243, 0.2)',
    borderColor: annotation.borderColor || '#2196F3',
    borderWidth: annotation.borderWidth || 1,
    radius: annotation.fontSize || 6,
    opacity: opacity,
    text: annotation.text,
    tooltip: annotation.tooltip
  }
}

function parseTime(timeStr: string): UTCTimestamp {
  // Convert string time to UTC timestamp
  const date = new Date(timeStr)
  return Math.floor(date.getTime() / 1000) as UTCTimestamp
}

function getLineStyleValue(style: string): number {
  const styleMap: { [key: string]: number } = {
    'solid': 0,
    'dotted': 1,
    'dashed': 2,
    'large_dashed': 3,
    'sparse_dotted': 4
  }
  return styleMap[style] || 0 // Default to solid
}

// Utility functions for annotation management
export function filterAnnotationsByTimeRange(
  annotations: Annotation[],
  startTime: string,
  endTime: string
): Annotation[] {
  const start = parseTime(startTime)
  const end = parseTime(endTime)
  
  return annotations.filter(annotation => {
    const time = parseTime(annotation.time)
    return time >= start && time <= end
  })
}

export function filterAnnotationsByPriceRange(
  annotations: Annotation[],
  minPrice: number,
  maxPrice: number
): Annotation[] {
  return annotations.filter(annotation => {
    return annotation.price >= minPrice && annotation.price <= maxPrice
  })
}

export function createAnnotationLayer(
  name: string,
  annotations: Annotation[] = []
): AnnotationLayer {
  return {
    name,
    annotations,
    visible: true,
    opacity: 1.0
  }
} 
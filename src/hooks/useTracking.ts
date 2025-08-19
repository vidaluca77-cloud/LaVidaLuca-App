'use client';

import { useEffect } from 'react';
import { performanceMonitor } from '@/monitoring/performance';
import { alertManager } from '@/monitoring/alerts';
import { setUserContext, setPageContext, trackUserActivity } from '../../sentry.client.config';
import { logger } from '@/lib/logger';

export interface UserInfo {
  id?: string;
  email?: string;
  username?: string;
  role?: string;
}

export interface PageInfo {
  page: string;
  section?: string;
  feature?: string;
}

/**
 * Hook for tracking user context and activities
 */
export const useUserTracking = (user: UserInfo | null) => {
  useEffect(() => {
    if (user) {
      // Set user context in Sentry
      setUserContext(user);
      
      // Log user session start
      logger.userAction('session_start', {
        user_id: user.id,
        user_role: user.role
      });
      
      trackUserActivity('User logged in', {
        user_id: user.id,
        user_role: user.role
      });
    } else {
      // Clear user context when logged out
      setUserContext({});
      logger.userAction('session_end');
      trackUserActivity('User logged out');
    }
  }, [user]);

  const trackAction = (action: string, metadata?: Record<string, any>) => {
    logger.userAction(action, {
      user_id: user?.id,
      ...metadata
    });
    
    trackUserActivity(action, {
      user_id: user?.id,
      ...metadata
    });
  };

  return { trackAction };
};

/**
 * Hook for tracking page views and navigation
 */
export const usePageTracking = (pageInfo: PageInfo) => {
  useEffect(() => {
    const startTime = performance.now();
    
    // Set page context
    setPageContext({
      ...pageInfo,
      loadTime: startTime
    });
    
    // Track page load performance
    performanceMonitor.start('page_load');
    
    // Log page view
    logger.info('Page viewed', {
      page: pageInfo.page,
      section: pageInfo.section,
      feature: pageInfo.feature
    });
    
    trackUserActivity('Page viewed', {
      page: pageInfo.page,
      section: pageInfo.section
    });
    
    // Cleanup function
    return () => {
      performanceMonitor.end('page_load', {
        page: pageInfo.page,
        section: pageInfo.section
      });
    };
  }, [pageInfo.page, pageInfo.section, pageInfo.feature]);
};

/**
 * Hook for tracking API calls and responses
 */
export const useApiTracking = () => {
  const trackApiCall = async <T>(
    url: string,
    options: RequestInit,
    fetchFn: () => Promise<T>
  ): Promise<T> => {
    const startTime = performance.now();
    const method = options.method || 'GET';
    
    logger.info('API call started', {
      url,
      method,
      timestamp: new Date().toISOString()
    });
    
    trackUserActivity('API call started', {
      url,
      method
    });
    
    try {
      const result = await fetchFn();
      const duration = performance.now() - startTime;
      
      // Record successful API call
      performanceMonitor.recordMetric('api_call', duration, {
        url,
        method,
        success: true,
        status: 200 // Assume success if no error
      });
      
      logger.apiCall(url, method, duration, 200, {
        success: true
      });
      
      trackUserActivity('API call completed', {
        url,
        method,
        duration_ms: duration,
        success: true
      });
      
      return result;
    } catch (error) {
      const duration = performance.now() - startTime;
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      
      // Record failed API call
      performanceMonitor.recordMetric('api_call', duration, {
        url,
        method,
        success: false,
        error: errorMessage
      });
      
      logger.apiCall(url, method, duration, 0, {
        success: false,
        error: errorMessage
      });
      
      // Alert for API errors
      alertManager.error(`API call failed: ${method} ${url}`, {
        url,
        method,
        error: errorMessage,
        duration_ms: duration
      });
      
      trackUserActivity('API call failed', {
        url,
        method,
        duration_ms: duration,
        error: errorMessage
      });
      
      throw error;
    }
  };

  return { trackApiCall };
};

/**
 * Hook for tracking form interactions
 */
export const useFormTracking = (formName: string) => {
  const trackFormStart = () => {
    logger.userAction('form_started', { form_name: formName });
    trackUserActivity('Form started', { form_name: formName });
  };

  const trackFormField = (fieldName: string, value?: string) => {
    logger.userAction('form_field_changed', {
      form_name: formName,
      field_name: fieldName,
      has_value: !!value
    });
    
    trackUserActivity('Form field changed', {
      form_name: formName,
      field_name: fieldName
    });
  };

  const trackFormSubmit = (success: boolean, errorMessage?: string) => {
    const action = success ? 'form_submitted_success' : 'form_submitted_error';
    
    logger.userAction(action, {
      form_name: formName,
      error: errorMessage
    });
    
    trackUserActivity(success ? 'Form submitted successfully' : 'Form submission failed', {
      form_name: formName,
      error: errorMessage
    });
    
    if (!success && errorMessage) {
      alertManager.warning(`Form submission failed: ${formName}`, {
        form_name: formName,
        error: errorMessage
      });
    }
  };

  const trackFormAbandonment = (completedFields: string[]) => {
    logger.userAction('form_abandoned', {
      form_name: formName,
      completed_fields: completedFields,
      completion_rate: completedFields.length
    });
    
    trackUserActivity('Form abandoned', {
      form_name: formName,
      completed_fields_count: completedFields.length
    });
  };

  return {
    trackFormStart,
    trackFormField,
    trackFormSubmit,
    trackFormAbandonment
  };
};

/**
 * Hook for tracking click events and user interactions
 */
export const useInteractionTracking = () => {
  const trackClick = (elementType: string, elementId?: string, elementText?: string) => {
    logger.userAction('element_clicked', {
      element_type: elementType,
      element_id: elementId,
      element_text: elementText
    });
    
    trackUserActivity('Element clicked', {
      element_type: elementType,
      element_id: elementId
    });
  };

  const trackSearch = (query: string, resultsCount?: number) => {
    logger.userAction('search_performed', {
      query_length: query.length,
      results_count: resultsCount,
      has_results: (resultsCount || 0) > 0
    });
    
    trackUserActivity('Search performed', {
      query_length: query.length,
      results_count: resultsCount
    });
  };

  const trackDownload = (fileName: string, fileType: string) => {
    logger.userAction('file_downloaded', {
      file_name: fileName,
      file_type: fileType
    });
    
    trackUserActivity('File downloaded', {
      file_name: fileName,
      file_type: fileType
    });
  };

  const trackShare = (content: string, platform?: string) => {
    logger.userAction('content_shared', {
      content_type: content,
      platform: platform
    });
    
    trackUserActivity('Content shared', {
      content_type: content,
      platform: platform
    });
  };

  return {
    trackClick,
    trackSearch,
    trackDownload,
    trackShare
  };
};

/**
 * Hook for tracking errors and exceptions
 */
export const useErrorTracking = () => {
  const trackError = (error: Error, context?: string, severity: 'low' | 'medium' | 'high' = 'medium') => {
    logger.error('Client error occurred', {
      error: error.message,
      stack: error.stack,
      context: context,
      severity: severity
    });
    
    const alertType = severity === 'high' ? 'error' : 'warning';
    alertManager.addAlert(alertType, `Client error: ${error.message}`, {
      context: context,
      severity: severity,
      stack: error.stack
    });
    
    trackUserActivity('Error occurred', {
      error_message: error.message,
      context: context,
      severity: severity
    });
  };

  const trackWarning = (message: string, context?: Record<string, any>) => {
    logger.warn('Client warning', {
      message: message,
      ...context
    });
    
    alertManager.warning(message, context);
    
    trackUserActivity('Warning occurred', {
      message: message,
      ...context
    });
  };

  return {
    trackError,
    trackWarning
  };
};
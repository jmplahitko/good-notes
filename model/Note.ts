import type { ActionItem } from './ActionItem'

export interface Note {
	id: string;
	title: string;
	attendees?: string[];
	meetingStartTime?: Date;
	content: string;
	createdAt: Date;
	updatedAt: Date;
	actionItems: ActionItem[];
}
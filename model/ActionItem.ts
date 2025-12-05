export interface ActionItem {
	id?: string;
	title: string;
	createdAt?: Date;
	updatedAt?: Date;
	completedAt?: Date | null;
	noteId?: string;
	completed?: boolean;
}